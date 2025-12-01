import requests
from core.git_utils import create_branch_and_push

def create_pull_request(repo_url: str, new_branch: str, base_branch: str, gh_token: str, title: str, body: str) -> str:
    # repo_url: https://github.com/owner/repo.git
    clean = repo_url.rstrip("/").replace(".git", "")
    owner_repo = clean.split("github.com/")[-1]
    api_url = f"https://api.github.com/repos/{owner_repo}/pulls"

    headers = {
        "Authorization": f"token {gh_token}",
        "Accept": "application/vnd.github+json",
    }
    payload = {
        "title": title,
        "head": new_branch,
        "base": base_branch,
        "body": body,
    }
    resp = requests.post(api_url, headers=headers, json=payload)
    resp.raise_for_status()
    pr = resp.json()
    return pr.get("html_url", "")
