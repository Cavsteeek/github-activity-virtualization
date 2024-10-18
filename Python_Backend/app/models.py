from pydantic import BaseModel


class Commit(BaseModel):
    sha: str
    message: str
    author_name: str
    date: str


class Contributor(BaseModel):
    login: str
    contributions: int


class Issue(BaseModel):
    title: str
    state: str
    created_at: str


class PullRequest(BaseModel):
    title: str
    state: str
    created_at: str
