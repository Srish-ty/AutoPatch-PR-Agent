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

Welcome to **AutoPatch PR Agent**, an innovative tool engineered to bridge the gap between issue detection and resolution in software development. By integrating cutting-edge AI capabilities with GitHub's robust API, this agent analyzes codebases, generates precise patches, and automates the entire Pull Request (PR) lifecycle—from branching and committing to publishing—ensuring minimal human intervention.

This repository hosts the core implementation, including the main notebook, utility scripts, and documentation to get you started quickly.

---

## ✨ Key Features

* **🤖 Advanced AI Patch Generation**: Utilizes state-of-the-art LLMs (e.g., Google Gemini, OpenAI GPT-4) to comprehend intricate code structures, dependencies, and context. Generates syntactically accurate, tested patches with minimal hallucinations.
* **🚀 Fully Automated PR Workflow**: End-to-end automation covering git operations—branch creation, patch application, commit staging, remote pushing, and PR submission—with intelligent conflict resolution and rollback mechanisms.
* **🛠️ Extensible Tool Integration**: Supports function calling for file manipulation, API interactions, and custom tools (e.g., linting, testing). Easily extendable via plugins for specialized tasks like database migrations or cloud deployments.
* **📝 Comprehensive Logging & Transparency**: Real-time, verbose logging with progress indicators, error diagnostics, and direct links to created PRs. Includes audit trails for compliance and debugging.
* **🔒 Security-First Design**: Implements token-based authentication, rate limiting, and sandboxed execution to prevent unauthorized access or malicious code injection.
* **🌐 Multi-Provider LLM Support**: Flexible configuration for various AI models, with fallback options and cost optimization strategies.
* **📊 Analytics & Insights**: Optional integration with monitoring tools to track patch success rates, time-to-resolution, and AI model performance metrics.

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

1. **Initialization & Authentication**:
   - Establishes secure connections to the target GitHub repository using a Personal Access Token (PAT).
   - Initializes the chosen LLM with API keys and model parameters (e.g., temperature, max tokens).

2. **Task Analysis & Planning**:
   - Parses the input task or issue (e.g., from a GitHub Issue, user prompt, or CI trigger).
   - Leverages the LLM to analyze the codebase via repository scanning, identifying relevant files, functions, and potential conflicts.

3. **Patch Generation**:
   - The AI crafts targeted code modifications, ensuring adherence to coding standards, best practices, and existing project conventions.
   - Incorporates unit tests or validation steps if configured, using tools like pytest or custom scripts.

4. **Execution & Publishing**:
   - Creates a feature branch with a descriptive name (e.g., `auto-patch/fix-issue-123`).
   - Applies patches atomically, with automatic staging and committing.
   - Pushes changes to the remote repository.
   - Generates a PR with a detailed title, body (including change summaries and AI-generated descriptions), and optional reviewers/assignees.
   - Handles edge cases like merge conflicts by retrying with refined patches or escalating to human review.

5. **Post-Processing & Feedback**:
   - Logs the outcome, including PR URLs and any warnings.
   - Optionally triggers downstream actions, such as CI builds or notifications via webhooks.

This process is encapsulated in the main notebook, but can be adapted for headless execution in production environments.

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
- **Optional Tools**: Docker for containerized runs, or IDEs like PyCharm for advanced debugging.

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

# Troubleshooting
- API Rate Limits: Monitor usage and implement retries with exponential backoff.
- Merge Conflicts: The agent attempts auto-resolution; otherwise, it logs for manual intervention.
- LLM Errors: Switch models or adjust prompts in prompts.py.

## 🤝 Contributing
We thrive on community contributions! Whether it's bug fixes, feature requests, or documentation improvements, your input is invaluable.

- Fork the Repository: Click the "Fork" button on GitHub.
- Create a Feature Branch: git checkout -b feature/YourAmazingFeature.
- Make Changes: Follow our Contributing Guidelines for coding standards and testing.
- Commit & Push: git commit -m 'Add YourAmazingFeature' and git push origin feature/YourAmazingFeature.
- Submit a PR: Open a Pull Request with a clear description. We'll review promptly!
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
