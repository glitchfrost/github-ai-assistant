from pydantic import BaseModel

class CodeFile(BaseModel):
    fileName: str
    content: str


class IndexRepositoryRequest(BaseModel):
    repoName: str
    files: list[CodeFile]


class AskRequest(BaseModel):
    repoName: str
    question: str