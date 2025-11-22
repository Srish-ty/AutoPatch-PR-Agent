# AutoPatch PR Agent

AutoPatch PR Agent is an AI-powered multi-agent system that automatically scans a repository, detects code style issues, fixes them, and creates a pull request with the corrected code. It helps developers and open-source contributors save time by automating repetitive cleanup tasks like formatting, unused imports, naming issues, and minor code smells.

The project is built for the Kaggle 5-Day AI Agents Intensive Capstone and demonstrates the use of multi-agent workflows, MCP tools, GitHub API integration, and LLM-powered code transformations.

---

## 🚀 Features

- Automatic repo scanning  
- Linting with Ruff / ESLint / Prettier  
- AI-generated code patches  
- Automatic file rewriting  
- Branch creation + commit  
- Pull Request creation using GitHub token  
- Multi-agent workflow  
- MCP tool integration  
- Basic memory for project style preferences  
- Clean logs for observability  

---

## 🧠 How It Works

1. **User inputs** a GitHub repo URL, base branch, and a personal access token (PAT).  
2. Repo is **cloned locally**.  
3. **Repo Scanner Agent** detects which files need cleanup.  
4. **Style Analysis Agent** runs linters and collects issues.  
5. **Fix Generator Agent** uses LLM + lint results to rewrite the files cleanly.  
6. **PR Creator Agent**:
   - creates a new branch  
   - commits changes  
   - pushes the branch  
   - opens a pull request automatically  
7. User gets a **PR link + summary of fixes**.

---

## 🏗 Architecture

```
User Input → Agent Orchestrator
                |
        ┌───────┼────────────────────────┐
        ▼       ▼                        ▼
Repo Scanner   Style Analysis        Fix Generator
   Agent          Agent                 Agent
        \          |                    /
         \         |                   /
          ▼        ▼                  ▼
              MCP Tools Layer
 (repo_tool, lint_tool, git_tool, github_tool)
                     |
                     ▼
               GitHub API (PR creation)
```

---

## 🔁 Workflow

1. Enter repo URL + token  
2. Clone repo  
3. Scan files  
4. Run linters  
5. Generate patches  
6. Apply fixes  
7. Create branch  
8. Commit + push  
9. Open PR  
10. Output PR link  

---

## 📦 Project Structure

```
auto-patch-agent/
│
├── agents/
│   ├── orchestrator.py
│   ├── repo_scanner.py
│   ├── style_analysis.py
│   ├── fix_generator.py
│   └── pr_creator.py
│
├── mcp_server/
│   ├── server.py
│   ├── repo_tool.py
│   ├── lint_tool.py
│   ├── git_tool.py
│   └── github_tool.py
│
├── interface/
│   ├── cli.py
│   └── ui.py (optional)
│
├── core/
│   ├── memory.py
│   ├── config.py
│   └── utils.py
│
├── data/
│   └── memory.json
│
├── README.md
├── requirements.txt
└── main.py
```

---

## 🛠 Tech Stack

- Python  
- MCP server  
- LLM (Gemini or OpenAI)  
- GitHub REST API  
- Ruff, ESLint, Prettier  
- Git CLI  
- SQLite/JSON for memory  

---

## ⚙️ Setup

```bash
git clone https://github.com/<your-username>/auto-patch-agent
cd auto-patch-agent
pip install -r requirements.txt
python main.py
```

---

## 🔧 Usage

- Enter repo URL  
- Enter GitHub token  
- Choose base branch  
- Agent scans → fixes → opens a PR  
- Copy your pull request link  

---

## 📌 Limitations

- Cannot merge PR automatically  
- User must provide a GitHub token  
- Works best on small-medium repos  
- AI fixes are safe but should be reviewed manually  

---

## 🎯 Future Enhancements

- Security linting  
- Automatic PR review comments  
- Full CI integration  
- Patch confidence scoring  
- Deeper semantic refactoring  

---

## ✨ About

Built by Srishty, Kanak, and Dwipal as part of the Kaggle Agents Intensive Capstone Project 2025.  
This tool aims to simplify open-source contributions by reducing the effort needed to prepare clean, patch-ready pull requests.
