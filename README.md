<h1 align="center"> 🤖 AutoPatch PR Agent</h1>
<p align="center"><em>Agents Intensive - Capstone Project By Kaggle</em></p>

<p align="center">
   
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?style=for-the-badge&logo=jupyter&logoColor=white)](https://jupyter.org/)
[![GitHub](https://img.shields.io/badge/GitHub-API-black?style=for-the-badge&logo=github&logoColor=white)](https://github.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen?style=for-the-badge)](https://github.com/Srish-ty/AutoPatch-PR-Agent/blob/main/CONTRIBUTING.md)

</p>

> **Revolutionize your development workflow with an AI-powered agent that autonomously patches code issues and seamlessly submits Pull Requests to GitHub. Harness the power of Large Language Models (LLMs) to transform bug fixes into effortless automation.**

---

<p align="center"><img src="https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3YmEwZWJzdjJxY3NkbXg0a2t1NTZidms4MTJmaGZiZ3EwczBldXc2cCZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/78XCFBGOlS6keY1Bil/giphy.gif" alt="Descriptive Alt Text" width="600"></p>

## 📖 Overview

Welcome to AutoPatch PR Agent, like a helpful robot team that uses AI to make coding easier. It checks code for mistakes, fixes them, and shares the changes online. We built it using Google's tools and smart AI to show how AI can help with everyday tasks.We are using human-in-the-loop logic to ask the user if they want to do fixes once we display all the changes, ensuring transparency and control. The Auto Patch PR Agent is a modular, multi-agent AI system designed to streamline software development workflows. Leveraging Google's ADK and Gemini LLM, it intelligently handles end-to-end code quality tasks—from repository cloning to PR submission. This project demonstrates advanced agent concepts, making it a standout example of AI-driven automation.

---

## ✨ Key Features

- **Repository Cloning**: Supports cloning public or private GitHub repos with optional branch checkout and token authentication.
- **Linting**: Uses Ruff to scan Python files for issues (e.g., style, errors).
- **Issue Tracking**: Stores linter issues in an in-memory artifact store with reference IDs.
- **Automated Fixes**: AI-driven fixes for issues, with safeguards to avoid problematic changes.
- **PR Creation**: Automatically creates a new branch, commits changes, pushes to GitHub, and opens a PR.
- **Observability**: Includes logging for tracing and metrics.
- **Scalability**: Built with ADK for multi-agent workflows, supporting async operations.
- **Memory and Sessions**: In-memory session service and memory bank for adaptive learning.

---

## 🔒 Safety & Security

AutoPatch PR Agent prioritizes security to ensure safe and responsible AI-assisted development. We conduct regular audits and encourage community reporting of vulnerabilities.

<details>
<summary><b>Click to expand safety findings</b></summary>

- **Potential Risks**: As with any AI tool, there is a risk of generating incorrect or insecure code patches. Always review PRs before merging.
- **Mitigations**: The agent includes built-in validation steps, such as running tests post-patch and limiting scope to specified files.
- **Best Practices**: Use in controlled environments, monitor API usage, and avoid applying patches to production code without human oversight.
- **Reporting**: If you discover security issues, please report them via [GitHub Issues](https://github.com/Srish-ty/AutoPatch-PR-Agent/issues) with the "security" label.

</details>

---

## ⚙️ How It Works

The AutoPatch PR Agent operates through a sophisticated pipeline designed for reliability and efficiency:

<details>
<summary><b>Click to expand safety findings</b></summary>

- **Setup**: Loads environment variables, configures logging, and initializes ADK components.
- **Agents**:
   - **RepoCloner**: Uses clone_repository to clone and optionally checkout a branch.
   - **Analyzer**: Runs run_linter_and_store to lint Python files and store issues in ARTIFACT_STORE.
   - **Fixer**: Processes issues, reads file content, and applies fixes using write_file. Outputs status via file_fixing_status schema.
   - **Publisher**: Uses create_github_pr to create a branch, commit, push, and open a PR.
- **Async Runner**: Manages agent interactions asynchronously with session persistence.
- **Utilities**:
   - **scan_files**: Discovers Python files.
   - **fetch_issue_batch**: Retrieves issues in batches.
   - **display_artifact_changes**: Prints a summary of changes.
   - Error handling for cloning, pushing, and API calls.
- **Memory**: ARTIFACT_STORE for issues, MEMORY_BANK for learning (e.g., storing last issues).

</details>

## 🚀 Getting Started

---

### Prerequisites

Before diving in, ensure you have the following:

- **Python 3.10+**: Required for compatibility with modern LLM libraries and async operations.
- **Jupyter Notebook** or **Google Colab**: For interactive execution and prototyping. Alternatively, use VS Code with Jupyter extensions for a richer IDE experience.
- **GitHub Account & PAT**: A Personal Access Token with `repo` and `pull_requests` scopes. Generate one [here](https://github.com/settings/tokens).
- **LLM API Access**: An API key for your preferred provider:
  - Google Gemini: Obtain from [Google AI Studio](https://makersuite.google.com/app/apikey).
  - OpenAI: Get from [OpenAI API](https://platform.openai.com/api-keys).
- **Git**: Installed and configured on your system for local repository operations.

---

### Installation

<details>
<summary><b>Click to expand safety findings</b></summary>

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Srish-ty/AutoPatch-PR-Agent.git
   cd AutoPatch-PR-Agent
2. Set Up a Virtual Environment (Recommended):
   ```bash
   python -m venv autopatch-env
   source autopatch-env/bin/activate  # On Windows: autopatch-env\Scripts\activate
3. Install Dependencies:
   ```bash
   pip install -r requirements.txt

---

### Key packages include:

- `gitpython`: For git operations.
- `requests`: For API interactions.
- `google-generativeai or openai`: For LLM integration.
- `jupyter`: For notebook execution.
- `Additional utilities`: pytest, black (for code formatting), and loguru (for advanced logging).

4. Configure Environment Variables: Create a .env file or set variables directly:

```bash
export GITHUB_TOKEN="your_github_token_here"
export GEMINI_API_KEY="your_gemini_api_key_here"  # Or OPENAI_API_KEY for OpenAI
export REPO_OWNER="target_repo_owner"
export REPO_NAME="target_repo_name"
```
For security, use a tool like python-dotenv to load from .env.

5. Verify Setup: Run a quick test:

```bash
python -c "import git, requests, google.generativeai; print('Setup complete!')"
```

</details>

## 💻 Usage

Running the Agent
- Launch the Notebook: Open auto-patch-pr-agent.ipynb in Jupyter or Colab.

- Configure Parameters: In the notebook's initialization cells, input or load:
   - Target repository details.
   - Task description (e.g., "Fix the null pointer exception in user authentication").
   - LLM settings (model, temperature, etc.).

- Execute the Main Loop: Run the cells sequentially. The final cell typically invokes await main() to start the process.

## Example Execution Output
A successful run might produce:

<details>
<summary><b>Click to expand safety findings</b></summary>
   
```text
[INFO] Initializing AutoPatch PR Agent...
[INFO] Analyzing codebase for task: 'Implement dark mode toggle'
[INFO] Generating patch using Gemini-1.5-Pro...
[INFO] Applying changes to files: ['src/components/Header.js', 'src/styles/theme.css']
[INFO] Creating branch: auto-patch/dark-mode-toggle
[INFO] Committing changes...
[INFO] Pushing to remote...
[INFO] Creating PR...
[SUCCESS] PR created successfully! View at: https://github.com/example/repo/pull/42
[INFO] PR Details: Title - "AutoPatch: Implement Dark Mode Toggle", Body - "Generated by AI: Added toggle button and CSS variables for seamless theme switching."
```
</details>

---

## 🤝 Contributing
We thrive on community contributions! Whether it's bug fixes, feature requests, or documentation improvements, your input is invaluable.

- **Fork the Repository**: Click the "Fork" button on GitHub.
- **Create a Feature Branch**: git checkout -b feature/YourAmazingFeature.
- **Make Changes**: Follow our Contributing Guidelines for coding standards and testing.
- **Commit & Push**: git commit -m 'Add YourAmazingFeature' and git push origin feature/YourAmazingFeature.
- **Submit a PR**: Open a Pull Request with a clear description. We'll review promptly!
For major changes, start a discussion in Issues.

---
👥 Contributors
This project is a collaborative effort by:

- Kanakbaghel
- Srish-ty
- dwipalshrirao
  
We welcome new contributors—see the Contributing section above to get involved!

---
## Acknowledgments
- Inspired by advancements in AI-driven development tools.
- Thanks to the open-source community for libraries like GitPython and the GitHub API.
- Special shoutout to our contributors (Kanakbaghel, Srish-ty, dwipalshrirao) and early adopters for feedback and testing.

---
> _" Let’s learn, grow, and innovate — together! "_
<p align="center"><em>Crafted with ♥ by <strong>Our Team</strong>
