
from urllib.parse import quote, urlparse, urlunparse
from datetime import datetime
import os
import shutil
import git
import re
from typing import  Optional
from urllib.parse import quote, urlparse, urlunparse
from datetime import datetime

from core.config import TEMP_REPOS_DIR


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _parse_github_owner_repo(url: str) -> Optional[tuple]:
    m = re.search(r"github\.com[:/](?P<owner>[^/]+)/(?P<repo>[^/.]+)", url or "")
    if not m:
        return None
    return m.group("owner"), m.group("repo").replace(".git", "")


def create_github_pr(local_path: str, repo_url: str, github_token: str = "") -> str:
    """
    Create a branch, push it, and open a PR. Returns PR URL or an error message.
    This is a simplified but functional rework of the original logic with clearer steps.
    """
    import requests

    try:
        repo = git.Repo(local_path)
    except Exception as e:
        return f"Error opening repo at {local_path}: {e}"

    try:
        current_branch = repo.active_branch.name
    except TypeError:
        return "Error: repository in detached HEAD; cannot determine current branch."
    except Exception as e:
        return f"Error determining current branch: {e}"

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    safe_branch = re.sub(r'[^A-Za-z0-9._-]+', '-', current_branch).strip('-')
    new_branch = f"fix-issues-{safe_branch}-{timestamp}"

    try:
        new_ref = repo.create_head(new_branch, commit=repo.head.commit)
        new_ref.checkout()
        if repo.is_dirty(untracked_files=True):
            repo.git.add("--all")
            repo.index.commit(f"Auto-fixes committed by tool on {timestamp}")
    except Exception as e:
        return f"Error creating/checking out branch '{new_branch}': {e}"

    try:
        origin = repo.remotes.origin
    except Exception:
        return "Error: remote 'origin' not found."

    owner_repo = _parse_github_owner_repo(repo_url) or _parse_github_owner_repo(origin.url)
    owner, repo_name = (owner_repo + (None,))[:2] if owner_repo else (None, None)

    auth_user = None
    headers = {"Accept": "application/vnd.github+json"}
    if github_token and owner and repo_name:
        headers["Authorization"] = f"token {github_token}"
        try:
            uresp = requests.get("https://api.github.com/user", headers=headers, timeout=10)
            if uresp.status_code == 200:
                auth_user = uresp.json().get("login")
            else:
                return f"Error: token authentication failed: {uresp.status_code} {uresp.text}"
            # quick permission check
            repo_api = f"https://api.github.com/repos/{owner}/{repo_name}"
            resp = requests.get(repo_api, headers=headers, timeout=10)
            if resp.status_code == 200:
                perms = resp.json().get("permissions", {})
                if not perms.get("push", False):
                    private = resp.json().get("private", False)
                    scope_hint = "repo (full 'repo' scope required for private repositories)" if private else "public_repo (or 'repo')"
                    return (f"Token authenticated as '{auth_user}' but does NOT have push access to {owner}/{repo_name}.\n"
                            f"Likely causes: token scope/membership issues. Repo permissions: {perms}")
        except Exception as e:
            return f"Error checking token/permissions: {e}"

    pushed = False
    try:
        origin.push(refspec=f"{new_branch}:{new_branch}", set_upstream=True)
        pushed = True
    except Exception:
        # try authenticated remote URL if token provided
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
            except Exception as e:
                user_hint = f" (token user: '{auth_user}')" if auth_user else ""
                return (f"Error pushing branch with token-authenticated remote: {e}{user_hint}")
            finally:
                try:
                    origin.set_url(orig_url)
                except Exception:
                    pass
        else:
            try:
                repo.git.push("--set-upstream", "origin", new_branch)
                pushed = True
            except Exception as e:
                user_hint = f" (token user: '{auth_user}')" if auth_user else ""
                return f"Error pushing branch '{new_branch}': {e}{user_hint}"

    if not pushed:
        return f"Branch '{new_branch}' created locally but push failed."

    if not github_token:
        return f"Branch created and pushed: {new_branch}. No token provided to create PR. Base: {current_branch}"

    if not owner or not repo_name:
        return "Error: cannot parse owner and repo name."

    # prefer current_branch as base, fallback to repo default if needed
    base_branch = current_branch
    try:
        br_resp = requests.get(f"https://api.github.com/repos/{owner}/{repo_name}/branches/{base_branch}", headers=headers, timeout=10)
        if br_resp.status_code != 200:
            repo_meta = requests.get(f"https://api.github.com/repos/{owner}/{repo_name}", headers=headers, timeout=10)
            if repo_meta.status_code == 200:
                base_branch = repo_meta.json().get("default_branch") or base_branch
    except Exception:
        pass

    head_branch = new_branch
    try:
        if auth_user and auth_user != owner:
            check_upstream = requests.get(f"https://api.github.com/repos/{owner}/{repo_name}/branches/{new_branch}", headers=headers, timeout=10)
            if check_upstream.status_code != 200:
                head_branch = f"{auth_user}:{new_branch}"
    except Exception:
        pass

    api_url = f"https://api.github.com/repos/{owner}/{repo_name}/pulls"
    payload = {"title": f"Auto-fix: {new_branch}", "head": head_branch, "base": base_branch, "body": "Automated fixes created by tool."}
    try:
        resp = requests.post(api_url, json=payload, headers=headers, timeout=15)
    except Exception as e:
        return f"Error calling GitHub API to create PR: {e}"

    if resp.status_code in (200, 201):
        pr = resp.json()
        pr_url = pr.get("html_url", str(pr))
        try:
            repo.git.checkout(current_branch)
        except Exception as e:
            return f"{pr_url} (PR created; failed to checkout back to '{current_branch}': {e})"
        return pr_url
    elif resp.status_code == 422:
        return "Error creating PR: 422 Validation Failed. Ensure base/head are correct."
    else:
        return f"Error creating PR: {resp.status_code} {resp.text}"
    

def clone_repository(repo_url: str, github_token: str = "", branch: str = "") -> str:
    """Clone a GitHub repository to a local temp dir and optionally checkout a branch.

    Returns the local path on success or an error string on failure.
    """
    repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
    local_path = os.path.abspath(os.path.join(TEMP_REPOS_DIR, repo_name))
    if os.path.exists(local_path):
        shutil.rmtree(local_path)
    ensure_dir(os.path.dirname(local_path))

    try:
        if github_token:
            auth_url = repo_url.replace("https://", f"https://{github_token}@")
            git.Repo.clone_from(auth_url, local_path)
        else:
            git.Repo.clone_from(repo_url, local_path)
    except Exception as e:
        return f"Error cloning repo: {e}"

    # If a branch was requested, try to checkout/create it.
    if branch:
        try:
            repo = git.Repo(local_path)
        except Exception as e:
            return f"Cloned to {local_path} but failed to open repo: {e}"

        # If branch exists locally, checkout it.
        local_branch_names = [b.name for b in repo.branches]
        if branch in local_branch_names:
            try:
                repo.git.checkout(branch)
                return local_path
            except Exception as e:
                return f"Cloned to {local_path} but failed to checkout local branch '{branch}': {e}"

        # Otherwise try to fetch origin and create a tracking branch from origin/{branch}
        try:
            origin = repo.remotes.origin
            origin.fetch()
            origin_ref = f"origin/{branch}"
            remote_refs = [r.name for r in repo.refs]
            if origin_ref in remote_refs:
                try:
                    repo.create_head(branch, repo.refs[origin_ref]).set_tracking_branch(repo.refs[origin_ref])
                    repo.git.checkout(branch)
                    return local_path
                except Exception as e:
                    return f"Cloned to {local_path} but failed to create/track branch '{branch}': {e}"
            else:
                return f"Error: Branch '{branch}' not found locally or on origin after clone."
        except Exception as e:
            return f"Cloned to {local_path} but failed to fetch origin to find branch '{branch}': {e}"

    # No branch requested, return cloned path
    return local_path