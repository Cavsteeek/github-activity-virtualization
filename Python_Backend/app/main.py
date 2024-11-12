from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests

from .services import (
    fetch_commits,
    fetch_contributors,
    fetch_issues,
    fetch_pull_requests,
    calculate_commit_frequency,
    count_issues,
    count_pull_requests,
)

from typing import List


gapp = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:8000",
]

gapp.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Endpoint to get commit frequency
@gapp.get("/commit_frequency")
async def get_commit_frequency(owner: str, repo: str):
    commits = await fetch_commits(owner, repo)
    frequency = calculate_commit_frequency(commits)
    return frequency


@gapp.get("/check_repo")
async def check_repo(owner: str, repo: str):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    response = requests.get(url)

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Repository not found")

    return {"message": "Repository exists"}


# Endpoint to get issue counts
@gapp.get("/issue_counts")
async def get_issue_counts(owner: str, repo: str):
    issues = await fetch_issues(owner, repo)
    counts = count_issues(issues)
    return counts


# Endpoint to get pull request counts
@gapp.get("/pull_request_counts")
async def get_pull_request_counts(owner: str, repo: str):
    pull_requests = await fetch_pull_requests(owner, repo)
    counts = count_pull_requests(pull_requests)
    return counts


# Endpoint to get commit data
@gapp.get("/commits")
async def get_commits(owner: str, repo: str):
    return await fetch_commits(owner, repo)


# Endpoint to get contributor data
@gapp.get("/contributors")
async def get_contributors(owner: str, repo: str):
    return await fetch_contributors(owner, repo)


# Endpoint to get issues and pull request data
@gapp.get("/issues")
async def get_issues(owner: str, repo: str):
    return await fetch_issues(owner, repo)


# Endpoint to get pull request data
@gapp.get("/pull_requests")
async def get_pull_requests(owner: str, repo: str):
    return await fetch_pull_requests(owner, repo)
