from fastapi import FastAPI
from language_detector import get_language
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

from models import (
    IndexRepositoryRequest,
    AskRequest
)

from chroma_manager import (
    collection
)

from embedding_service import (
    generate_embedding
)

from ollama_service import (
    ask_llama
)

app = FastAPI()


# =====================================================
# FILE FILTER
# Skip files that add noise and slow indexing down
# =====================================================

# Extensions worth indexing
ALLOWED_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx",
    ".java", ".kt", ".go", ".rs", ".rb",
    ".cpp", ".c", ".cs", ".php",
    ".html", ".css", ".scss", ".sass",
    ".json", ".yaml", ".yml",
    ".md", ".txt", ".sh", ".sql",
}

# Directory names to skip entirely
SKIP_DIRS = {
    "node_modules", ".git", "dist", "build",
    "__pycache__", ".next", "vendor", "coverage",
    ".idea", ".vscode", "venv", "env", ".env",
    "public", "static", "assets", "images",
    "fonts", "icons", "media",
}

# File patterns to skip
SKIP_PATTERNS = [
    r"\.min\.(js|css)$",       # minified files
    r"package-lock\.json$",    # lock files
    r"yarn\.lock$",
    r"poetry\.lock$",
    r"\.map$",                  # source maps
    r"\.svg$",                  # SVG images
    r"\.png$", r"\.jpg$",
    r"\.jpeg$", r"\.gif$",
    r"\.ico$", r"\.woff",
    r"\.ttf$", r"\.eot$",
]

MAX_FILE_SIZE_CHARS = 15_000   # skip files larger than this
MAX_FILES_TO_INDEX  = 500      # cap total files per repo


def should_skip_file(file_name: str, content: str) -> bool:
    """Return True if this file should be excluded from indexing."""
    lower = file_name.lower()

    # Check blocked directory segments
    parts = lower.replace("\\", "/").split("/")
    if any(part in SKIP_DIRS for part in parts):
        return True

    # Check extension
    ext = "." + lower.rsplit(".", 1)[-1] if "." in lower else ""
    if ext and ext not in ALLOWED_EXTENSIONS:
        return True

    # Check skip patterns
    for pattern in SKIP_PATTERNS:
        if re.search(pattern, lower):
            return True

    # Skip oversized files (minified / generated)
    if len(content) > MAX_FILE_SIZE_CHARS:
        return True

    # Skip effectively empty files
    if len(content.strip()) < 30:
        return True

    return False


# =====================================================
# CHUNKING
# =====================================================

def split_into_chunks(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += (chunk_size - overlap)
    return chunks


# =====================================================
# METADATA EXTRACTION
# =====================================================

def extract_metadata(content, file_name):

    language = get_language(file_name)

    class_match = re.search(
        r'class\s+(\w+)',
        content
    )

    interface_match = re.search(
        r'interface\s+(\w+)',
        content
    )

    function_matches = re.findall(
        r'(?:public|private|protected)?\s*(?:static)?\s*[\w\<\>\[\]]*\s+(\w+)\s*\(',
        content
    )

    return {
        "fileName": file_name,
        "language": language,
        "className": (
            class_match.group(1)
            if class_match
            else interface_match.group(1)
            if interface_match
            else "Unknown"
        ),
        "type": (
            "interface"
            if interface_match
            else "class"
        ),
        "methods": ",".join(function_matches[:20])
    }


# =====================================================
# HOME
# =====================================================

@app.get("/")
def home():
    return {"message": "AI Service Running"}


# =====================================================
# INDEX REPOSITORY
# =====================================================

def _index_single_file(file, repo_name: str):
    """
    Embed and store all chunks for one file.
    Returns the fileName on success, None on failure.
    """
    try:
        metadata = extract_metadata(file.content, file.fileName)
        metadata["repoName"] = repo_name

        chunks = split_into_chunks(file.content)

        ids        = []
        embeddings = []
        documents  = []
        metadatas  = []

        for index, chunk in enumerate(chunks):
            embedding = generate_embedding(chunk)
            chunk_metadata = {**metadata, "chunkIndex": index}

            ids.append(f"{repo_name}_{file.fileName}_{index}")
            embeddings.append(embedding)
            documents.append(chunk)
            metadatas.append(chunk_metadata)

        # Batch-add all chunks for this file in one call
        if ids:
            collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas,
            )

        return file.fileName

    except Exception as e:
        print(f"Failed to index {file.fileName}: {e}")
        return None


@app.post("/index-repository")
def index_repository(request: IndexRepositoryRequest):

    # ── 1. FILTER OUT NOISE FILES ──────────────────────
    all_files = request.files
    total_received = len(all_files)

    filtered_files = [
        f for f in all_files
        if not should_skip_file(f.fileName, f.content)
    ]

    # ── 2. CAP TOTAL FILES ─────────────────────────────
    if len(filtered_files) > MAX_FILES_TO_INDEX:
        print(
            f"[index] Capping {len(filtered_files)} → "
            f"{MAX_FILES_TO_INDEX} files"
        )
        filtered_files = filtered_files[:MAX_FILES_TO_INDEX]

    skipped = total_received - len(filtered_files)
    print(
        f"[index] {total_received} received | "
        f"{skipped} skipped | "
        f"{len(filtered_files)} to index"
    )

    # ── 3. CONCURRENT EMBEDDING ────────────────────────
    indexed_count  = 0
    failed_count   = 0
    indexed_files  = []

    # Use 4 threads — safe for most local Ollama setups.
    # Increase to 8 if your embedding model handles parallel requests.
    MAX_WORKERS = 4

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(_index_single_file, f, request.repoName): f.fileName
            for f in filtered_files
        }
        for future in as_completed(futures):
            result = future.result()
            if result:
                indexed_count += 1
                indexed_files.append(result)
            else:
                failed_count += 1

    print(
        f"[index] Done — {indexed_count} indexed, "
        f"{failed_count} failed"
    )

    return {
        "message": "Repository Indexed",
        "totalReceived": total_received,
        "skipped": skipped,
        "filesIndexed": indexed_count,
        "failed": failed_count,
    }


# =====================================================
# ASK QUESTION
# =====================================================

@app.post("/ask")
def ask_question(request: AskRequest):

    print("QUESTION =", request.question)
    print("REPO =", request.repoName)

    question_embedding = generate_embedding(request.question)

    results = None

    # ============================================
    # STEP 1 — CHECK IF QUESTION CONTAINS A FULL PATH
    # e.g. "Explain javascript/oojs/index.html"
    # If so, use that path directly for an exact match.
    # ============================================

    # Stopwords — common words that should never be treated as targets
    STOPWORDS = {
        "the", "a", "an", "this", "that", "me", "my", "our",
        "its", "your", "their", "how", "what", "why", "where",
        "when", "which", "all", "any", "some", "each", "every",
        "file", "code", "class", "method", "function", "folder",
        "directory", "repo", "repository", "project", "app",
        "structure", "overview", "summary", "list",
    }

    # Pattern 0 — full or partial path with slashes
    # e.g. "javascript/oojs/index.html" or "oojs/index.html"
    path_match = re.search(
        r"(?:explain|describe|what\s+is|tell\s+me\s+about|show\s+me|summarize|walk\s+me\s+through)?\s*"
        r"((?:[A-Za-z0-9_\-]+/)+[A-Za-z0-9_\-]+\.[A-Za-z0-9]{1,10})",
        request.question,
        re.IGNORECASE
    )

    # Pattern A — plain filename with extension (e.g. index.html, App.tsx)
    file_name_match = re.search(
        r"(?:what\s+is|what\s+does|explain|describe|tell\s+me\s+about|how\s+does|show\s+me|summarize|walk\s+me\s+through)?\s*"
        r"([A-Za-z0-9_\-]+\.[A-Za-z0-9]{1,10})",
        request.question,
        re.IGNORECASE
    )

    # Pattern B — plain class/component name without extension
    class_name_match = re.search(
        r"(?:what\s+is|what\s+does|explain|describe|tell\s+me\s+about|how\s+does|show\s+me|summarize|walk\s+me\s+through)\s+"
        r"([A-Za-z0-9_]+)",
        request.question,
        re.IGNORECASE
    )

    target_path      = path_match.group(1).strip() if path_match else None
    target_filename  = file_name_match.group(1).strip() if (file_name_match and not target_path) else None
    raw_classname    = class_name_match.group(1).strip() if class_name_match else None
    target_classname = raw_classname if (
        raw_classname and raw_classname.lower() not in STOPWORDS
    ) else None

    print("TARGET PATH   =", target_path)
    print("TARGET FILE   =", target_filename)
    print("TARGET CLASS  =", target_classname)

    # ============================================
    # STEP 2 — FETCH ALL DOCS FOR THIS REPO
    # (single round-trip; filter in Python)
    # ============================================

    if target_path or target_filename or target_classname:
        try:
            all_results = collection.get(
                where={"repoName": {"$eq": request.repoName}}
            )
        except Exception as e:
            print(f"Collection fetch failed: {e}")
            all_results = None

        if all_results and all_results.get("documents"):

            # Group chunks by their full fileName so we can detect ambiguity
            # { "path/to/index.html": [(doc, meta), ...], ... }
            file_groups: dict = {}

            for doc, meta in zip(
                all_results["documents"],
                all_results["metadatas"]
            ):
                stored_name  = meta.get("fileName", "")
                stored_class = meta.get("className", "")
                normalised   = stored_name.replace("\\", "/")
                basename     = normalised.split("/")[-1]

                matched = False

                # ── full/partial path match ──
                if target_path:
                    if normalised.lower().endswith(target_path.lower()):
                        matched = True

                # ── plain filename match ──
                elif target_filename:
                    if basename.lower() == target_filename.lower():
                        matched = True

                # ── class / stem name match ──
                elif target_classname:
                    stem = basename.rsplit(".", 1)[0]
                    if (
                        stem.lower() == target_classname.lower()
                        or stored_class.lower() == target_classname.lower()
                    ):
                        matched = True

                if matched:
                    file_groups.setdefault(normalised, []).append((doc, meta))

            # ── AMBIGUITY CHECK ──────────────────────────────────
            # If more than one distinct file matched (e.g. 30 index.html files),
            # don't dump all chunks to the LLM — ask the user to clarify.
            if len(file_groups) > 1:
                file_list = "\n".join(f"- {p}" for p in sorted(file_groups.keys()))
                clarification = (
                    f"Found **{len(file_groups)} files** named "
                    f"`{target_path or target_filename or target_classname}` "
                    f"in this repository. Please specify which one you mean "
                    f"by including part of the path, e.g.:\n\n"
                    f"*Explain javascript/oojs/index.html*\n\n"
                    f"**All matching files:**\n{file_list}"
                )
                return {
                    "repoName": request.repoName,
                    "question": request.question,
                    "answer": clarification,
                    "filesUsed": sorted(file_groups.keys()),
                    "sourceCount": len(file_groups),
                    "ambiguous": True,
                }

            # ── SINGLE FILE MATCHED ──────────────────────────────
            if file_groups:
                matched_docs  = []
                matched_metas = []
                for docs_metas in file_groups.values():
                    for doc, meta in docs_metas:
                        matched_docs.append(doc)
                        matched_metas.append(meta)

                print(f"EXACT MATCH FOUND: 1 file, {len(matched_docs)} chunks")
                results = {
                    "documents": [matched_docs],
                    "metadatas": [matched_metas],
                }
            else:
                print("No exact match — falling back to vector search")

    # ============================================
    # VECTOR SEARCH FALLBACK
    # ============================================

    if results is None:
        print("FALLING BACK TO VECTOR SEARCH")
        try:
            results = collection.query(
                query_embeddings=[question_embedding],
                n_results=12,
                where={"repoName": {"$eq": request.repoName}}
            )
        except Exception as e:
            print(f"Vector search failed: {e}")
            return {
                "repoName": request.repoName,
                "question": request.question,
                "answer": f"Search failed: {str(e)}",
                "filesUsed": [],
                "sourceCount": 0
            }

    # ============================================
    # NO RESULTS FOUND
    # ============================================

    if (
        not results.get("documents")
        or not results["documents"][0]
    ):
        return {
            "repoName": request.repoName,
            "question": request.question,
            "answer": "Repository not indexed or no matching code found.",
            "filesUsed": [],
            "sourceCount": 0
        }

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    files_used = []
    context_parts = []

    for doc, meta in zip(documents, metadatas):
        if meta:
            if meta["fileName"] not in files_used:
                files_used.append(meta["fileName"])

            context_parts.append(
                f"""
FILE: {meta.get('fileName')}
CHUNK: {meta.get('chunkIndex')}

CLASS: {meta.get('className')}
TYPE: {meta.get('type')}

METHODS:
{meta.get('methods')}

CODE:
{doc}
"""
            )

    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""
You are an expert Senior Software Engineer, Software Architect, and Code Reviewer.

Analyze the repository using ONLY the provided code context.

If answering about a SPECIFIC FILE, use ONLY the code belonging to that file.

Do NOT pull in details from other files unless explicitly asked.

STRICT RULES

1. Use ONLY the provided repository context.

2. Never invent:
- classes / components / functions
- HTML elements or attributes not present
- CSS rules not present
- APIs or behavior

3. If the answer does not exist in the code, reply exactly:

Not found in repository code.

4. Never use:
- appears to be / seems to be / likely / probably
- can be inferred / might be / suggests / implies

5. Always mention exact:
- file names
- class names / component names
- function / method names
- HTML tags, IDs, class attributes (for HTML files)
- CSS selectors and properties (for CSS files)

6. Explain WHY this file or component exists.

7. Explain HOW it connects to other files or components.

8. Adapt your explanation to the file type:

   If HTML file:
   - List the page structure (head, body sections)
   - Mention all linked CSS and JS files
   - Describe key elements, IDs, and classes
   - Note forms, tables, or interactive elements

   If CSS file:
   - List key selectors and what they style
   - Note layout techniques used (flexbox, grid, etc.)

   If JavaScript file:
   - List functions / classes exported
   - Describe event listeners and DOM interactions

   If Java / Spring Boot:
   Controller → Service → Repository → Database

   If React / Vue:
   Component → Props → State → API calls

   If FastAPI / Python:
   Endpoint → Service → Database

ANSWER FORMAT

## What It Is

## Purpose

## Key Components

## How It Works

## Links / Dependencies

## Source File

## Summary

REPOSITORY CONTEXT

{context}

QUESTION

{request.question}

ANSWER
"""

    print("\n==============================")
    print("QUESTION")
    print(request.question)
    print("\nRETRIEVED FILES")
    for file_name in files_used:
        print(file_name)
    print("\nTOTAL FILES:", len(files_used))
    print("==============================")

    # FIX 3: Wrap ask_llama in try/except so errors return
    # a readable message instead of a 500 crash
    try:
        answer = ask_llama(prompt)
    except Exception as e:
        print(f"LLM call failed: {e}")
        return {
            "repoName": request.repoName,
            "question": request.question,
            "answer": f"LLM error: {str(e)}. Make sure Ollama is running and the model is pulled.",
            "filesUsed": files_used,
            "sourceCount": len(files_used)
        }

    return {
        "repoName": request.repoName,
        "question": request.question,
        "answer": answer,
        "filesUsed": files_used,
        "sourceCount": len(files_used)
    }


# =====================================================
# EXPLAIN FILE
# =====================================================

@app.get("/explain-file")
def explain_file(file_name: str):
    results = collection.get(where={"fileName": file_name})

    if not results or not results["documents"]:
        return {"error": "File not found"}

    content = results["documents"][0]

    prompt = (
        "Explain this source file.\n\n"
        "Include:\n"
        "1. Purpose\n"
        "2. Classes\n"
        "3. Methods\n"
        "4. Dependencies\n"
        "5. Design Patterns\n"
        "6. Important Logic\n\n"
        f"FILE CONTENT:\n\n{content}"
    )

    try:
        explanation = ask_llama(prompt)
    except Exception as e:
        return {"file": file_name, "explanation": f"LLM error: {str(e)}"}

    return {"file": file_name, "explanation": explanation}


# =====================================================
# GENERATE README
# =====================================================

@app.get("/generate-readme")
def generate_readme():
    data = collection.get()
    repository_code = "\n\n".join(data["documents"][:20])

    prompt = (
        "Generate a professional README.md.\n\n"
        "Include:\n"
        "- Project Overview\n"
        "- Features\n"
        "- Tech Stack\n"
        "- Installation\n"
        "- Usage\n"
        "- Project Structure\n\n"
        f"REPOSITORY:\n\n{repository_code}"
    )

    try:
        readme = ask_llama(prompt)
    except Exception as e:
        return {"readme": f"LLM error: {str(e)}"}

    return {"readme": readme}


# =====================================================
# DATABASE STATS
# =====================================================

@app.get("/stats")
def stats():
    sample = collection.get(limit=10)
    return {
        "documents": collection.count(),
        "sampleFiles": sample["metadatas"]
    }


# =====================================================
# BUG DETECTION
# =====================================================

@app.get("/detect-bugs")
def detect_bugs():
    data = collection.get()
    repository_code = "\n\n".join(data["documents"][:20])

    prompt = (
        "Analyze this repository.\n\n"
        "Find:\n"
        "- Potential Bugs\n"
        "- Null Pointer Risks\n"
        "- Security Vulnerabilities\n"
        "- Unused Code\n"
        "- Performance Issues\n"
        "- Missing Exception Handling\n\n"
        f"CODE:\n\n{repository_code}"
    )

    try:
        report = ask_llama(prompt)
    except Exception as e:
        return {"issues": f"LLM error: {str(e)}"}

    return {"issues": report}