# Git Standup Sloth

A local CLI that reads your recent git commits and writes your standup,
using an open-weight model running entirely on your machine.

<div align="center">
  <a href="https://www.youtube.com/watch?v=reR8oLTXelM">
    <img src="https://img.youtube.com/vi/reR8oLTXelM/maxresdefault.jpg" width="100%" alt="Git Standup Sloth Demo Video">
  </a>
</div>

## Why

Standup is 5-10 minutes of staring at `git log` every morning. A standup
also describes private work — client repos, internal paths, unreleased
features. This tool sends nothing over the network: the model is
open-weight and runs locally via Ollama.

## Screenshot

![standup output](screenshot.png)

## System Architecture

```mermaid
graph LR
    User([User]) -->|runs command| CLI[app.py CLI]

    subgraph Local Machine
        CLI -->|extracts commits| GitData[gitdata.py]
        GitData -->|git log --stat| Repo[(Local Git Repo)]
        Repo -->|commit history| GitData

        GitData -->|capped string 2500 chars| LLM[llm.py]
        LLM -->|prompt + context| Ollama[Ollama API]
        Ollama -->|local inference| Model[Qwen2.5-1.5B Model]

        Model -->|standup draft| Ollama
        Ollama -->|response| LLM
        LLM -->|formatted text| CLI
        
        CLI -->|copies to| Clipboard[(OS Clipboard)]
        CLI -->|prints| Output([Terminal Output])
    end
    
    classDef local fill:#f9f9f9,stroke:#333,stroke-width:2px;
    class CLI,GitData,LLM,Ollama,Model,Repo,Clipboard local;
```

## Setup

1. Install [Ollama](https://ollama.com/download)
2. `ollama pull qwen2.5:1.5b`
3. `pip install -r requirements.txt`

## Usage

```bash
python app.py                          # last 24h in current repo
python app.py --repo ../other-project  # specific repo
python app.py --since "1 week ago"     # weekly recap
python app.py --output standup.md      # save to file
```

Output is printed to the terminal and copied to your clipboard.

## How it works

`git log --stat` → strict prompt → `qwen2.5:1.5b` via Ollama → standup.

No API keys. No cloud. No data leaves your machine.

## Limitations

- 1.5B model can duplicate bullets and paraphrase loosely.
- Reads commit messages + diff stats only, not diff contents.
- Prompt is capped at 2,500 chars to keep the small model focused.

## Built with


> **Built with an open-weight model for the Hacktoberfest Open-Source AI Challenge: Week 3.**