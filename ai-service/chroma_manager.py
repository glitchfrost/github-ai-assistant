import chromadb

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="repository_code"
)


def search_code(question_embedding):

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=10
    )

    return results


def get_stats():

    return {
        "documents": collection.count()
    }