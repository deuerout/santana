# Market Research Agent

A working [CrewAI](https://github.com/crewAIInc/crewAI) crew that researches a market
segment and turns the findings into a polished, client-ready report.

## What it does

- **Agent 1 — `Market Researcher`**: analyzes market data and surfaces trends, customer
  preferences, growth opportunities, and strategic recommendations.
  - **Tool**: `MarketAnalysisTool`, a thin wrapper around `SerperDevTool` that performs a
    live web search for the given market segment and labels the results as market
    analysis input for the agent.
- **Agent 2 — `Report Writer`**: takes the researcher's raw findings (via CrewAI task
  `context`, no new tool calls) and rewrites them as a Markdown report with an executive
  summary and clearly labeled sections — without inventing new facts.
- **Tasks**: (1) analyze a market segment (default: `Sustainable Technologies`, or pass
  your own on the command line), (2) write it up.
- **Crew**: a two-agent, sequential-process crew that runs both tasks in order and prints
  the final report.

## Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Provide API keys. Copy `.env.example` to `.env` and fill in your keys, or export them
   in your shell:

   - `OPENAI_API_KEY` — powers the agent's LLM calls (CrewAI defaults to OpenAI).
     Get one at https://platform.openai.com/api-keys
   - `SERPER_API_KEY` — powers `MarketAnalysisTool`'s web search.
     Get one at https://serper.dev/api-key

   ```bash
   cp .env.example .env
   # then edit .env
   ```

## Run it

```bash
python market_research_agent.py "Sustainable Technologies"
```

Omit the argument to use the default segment:

```bash
python market_research_agent.py
```

If either API key is missing, the script exits immediately with a clear message telling
you which one to set and where to get it, instead of failing deep inside a network call.

## Extending

- **Different LLM**: set `OPENAI_MODEL_NAME` (or configure a different provider per
  [CrewAI's LLM docs](https://docs.crewai.com/concepts/llms)) before running.
- **More agents/tasks**: add them in `build_market_research_crew()` in
  `market_research_agent.py` and wire them into the `Crew`. Use a task's `context=[...]`
  to hand it another task's output, the way `report_writing_task` consumes
  `trend_analysis_task`.
- **Different search backend**: swap `SerperDevTool` for another `crewai_tools` search
  tool, or implement a custom `BaseTool` subclass.
