import asyncio

from agents.orchestrator import run_pipeline

def main():
    repo_url = input("GitHub Repo URL: ").strip()
    gh_token = input("GitHub Token: ").strip()
    base_branch = input("Base branch (default: main): ").strip() or "main"

    asyncio.run(run_pipeline(repo_url, gh_token, base_branch))

if __name__ == "__main__":
    main()
