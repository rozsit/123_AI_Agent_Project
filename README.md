# AI Web Search Agent (GPT-5 + Tavily)

This project implements a real-time **AI Agent** capable of autonomous decision-making, web search, and evidence-based answering using **GPT‑5** and **Tavily Search API**.

Unlike a standard chatbot, this agent:
- Decides when to perform real‑time search
- Fetches live web results
- Aggregates and synthesizes information
- Responds with citations
- Maintains session memory
- Shows structured reasoning summaries

## Features

| Capability | Description |
|---|---|
Real-time data | Live information via Tavily API |
Autonomous tool use | Agent decides when to call tools |
Citations | Always includes 1–3 verifiable sources |
Reasoning mode | Displays model's thought summary |
Persistent context | Conversation memory within session |
Exit command | `exit` or `q` |

## Project Structure

```
project/
│
├─ agent.py
├─ .env
├─ requirements.txt
└─ env/  (virtual environment)
```

## Installation

### 1) Create virtual environment

```bash
python -m venv env
```

### 2) Activate (Windows PowerShell)

```powershell
.\env\Scripts\Activate.ps1
```

### 3) Install packages

```bash
pip install -r requirements.txt
```

## `.env` Example

Create a `.env` file in project root:

```
OPENAI_API_KEY=your_openai_key
TAVILY_API_KEY=your_tavily_key
```

> Never commit this file to GitHub.

## Run the Agent

```bash
python agent.py
```

### Example Prompts

```
What are the latest AI news? Provide sources.
What happened today in global markets?
What's the weather in Budapest right now?
exit
```

## Sample Agent Output

```
User: Latest AI news?

Assistant (thinking...)
 • real‑time data needed
 • invoking web search tool

Assistant:
Several AI breakthroughs reported today...
Sources:
- CNN
- ArsTechnica
- Reuters
```

## Requirements

- Python 3.10+
- OpenAI API key
- Tavily API key

## Future Extensions

- Web UI (Streamlit)
- Voice-controlled agent
- Scheduled email reports
- RAG document search
- Market monitoring bot

## Author

AI Web Agent Project — exploring real‑world autonomous LLM agents.

If you found this useful, ⭐ star the repo!
