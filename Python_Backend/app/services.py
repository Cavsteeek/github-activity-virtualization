import httpx
import os
from fastapi import HTTPException
from dotenv import load_dotenv
from .models import Commit, Contributor, Issue


load_dotenv()

API_URL = os.getenv("GITHUB_API_URL")
TOKEN = os.getenv("GITHUB_API_TOKEN")


if not API_URL:
    raise ValueError("API_URL is not set. Check your .env file.")
if not TOKEN:
    raise ValueError("GitHub API token is not set. Check your .env file.")

HEADERS = {"Authorization": f"token {TOKEN}"}


async def fetch_commits(owner: str, repo: str):
    url = f"{API_URL}{owner}/{repo}/commits"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail="Error fetching commits"
            )
        commits_data = response.json()
        return [
            Commit(
                sha=commit["sha"],
                message=commit["commit"]["message"],
                author_name=commit["commit"]["author"]["name"],
                date=commit["commit"]["author"]["date"],
            )
            for commit in commits_data
        ]


async def fetch_contributors(owner: str, repo: str):
    url = f"{API_URL}{owner}/{repo}/contributors"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail="Error fetching contributors"
            )
        contributors_data = response.json()
        return [
            Contributor(
                login=contributor["login"], contributions=contributor["contributions"]
            )
            for contributor in contributors_data
        ]


async def fetch_issues(owner: str, repo: str):
    url = f"{API_URL}{owner}/{repo}/issues"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail="Error fetching issues"
            )
        issues_data = response.json()
        return [
            Issue(
                title=issue["title"],
                state=issue["state"],
                created_at=issue["created_at"],
            )
            for issue in issues_data
        ]
