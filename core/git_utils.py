# Git utils
# Local git operations
import os
from pathlib import Path
from typing import Optional

from git import Repo  # pip install GitPython
from urllib.parse import urlparse, urlunparse, quote

def write_file(file_path: str, content: str) -> str:
    try:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as fh:
            fh.write(content)
        return f"Updated {file_path}"
    except Exception as e:
        return f"Error writing {file_path}: {e}"

def clone_repo(repo_url: str, dest_dir: str, branch: Optional[str] = None) -> str:
    os.makedirs(dest_dir, exist_ok=True)
    repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
    local_path = os.path.join(dest_dir, repo_name)
    if not os.path.exists(local_path):
        repo = Repo.clone_from(repo_url, local_path)
    else:
        repo = Repo(local_path)
    if branch:
        repo.git.checkout(branch)
    return local_path

def create_branch_and_push(repo_path: str, new_branch: str, github_token: Optional[str] = None) -> str:
    repo = Repo(repo_path)
    git = repo.git

    git.checkout("-b", new_branch)
    repo.git.add(A=True)
    repo.index.commit(f"chore: auto style fixes by agent")

    origin = repo.remote(name="origin")
    pushed = False
    try:
        origin.push(refspec=f"{new_branch}:{new_branch}", set_upstream=True)
        pushed = True
    except Exception:
        if github_token and origin.url and origin.url.startswith("http"):
            orig_url = origin.url
            try:
                token_enc = quote(github_token, safe='')
                parsed = urlparse(orig_url)
                host = parsed.hostname or ''
                port = f":{parsed.port}" if parsed.port else ''
                new_netloc = f"x-access-token:{token_enc}@{host}{port}"
                authed = parsed._replace(netloc=new_netloc)
                origin.set_url(urlunparse(authed))
                repo.git.push("--set-upstream", "origin", new_branch)
                pushed = True
            finally:
                try:
                    origin.set_url(orig_url)
                except Exception:
                    pass
    if not pushed:
        raise RuntimeError("Failed to push branch.")
    return new_branch
