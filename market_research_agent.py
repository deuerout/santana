import argparse
import os
import sys

from dotenv import load_dotenv

load_dotenv()

from crewai import Agent, Crew, Process, Task
from crewai_tools import SerperDevTool

REQUIRED_ENV_VARS = {
    "OPENAI_API_KEY": "https://platform.openai.com/api-keys",
    "SERPER_API_KEY": "https://serper.dev/api-key",
}


def check_environment() -> None:
    missing = [name for name in REQUIRED_ENV_VARS if not os.getenv(name)]
    if missing:
        lines = [f"Missing required environment variable(s): {', '.join(missing)}", ""]
        for name in missing:
            lines.append(f"  {name} -> get one at {REQUIRED_ENV_VARS[name]}")
        lines.append("")
        lines.append("Set them in your shell or in a .env file (see .env.example).")
        raise SystemExit("\n".join(lines))


class MarketAnalysisTool(SerperDevTool):
    name: str = "Market Analysis Tool"
    description: str = "Fetches and analyzes market data for a given market segment."

    def _run(self, market_segment: str) -> str:
        raw = super()._run(market_segment)
        return f"Comprehensive market analysis for '{market_segment}':\n{raw}"


def build_market_research_crew() -> Crew:
    tool = MarketAnalysisTool()

    market_researcher = Agent(
        role="Market Researcher",
        goal="Identify emerging market trends and provide actionable insights",
        verbose=True,
        memory=True,
        backstory=(
            "Armed with analytical prowess and a knack for spotting trends, "
            "you navigate through complex market data to unearth opportunities "
            "that help shape strategic decisions."
        ),
        tools=[tool],
    )

    trend_analysis_task = Task(
        description=(
            "Analyze the '{market_segment}' market segment. "
            "Identify current trends, customer preferences, and potential "
            "growth opportunities. Support each finding with data."
        ),
        expected_output=(
            "A structured report containing: "
            "(1) top 3-5 current trends, "
            "(2) key customer preferences, "
            "(3) growth opportunities with supporting evidence, "
            "(4) strategic recommendations."
        ),
        agent=market_researcher,
    )

    return Crew(
        agents=[market_researcher],
        tasks=[trend_analysis_task],
        process=Process.sequential,
        verbose=True,
    )


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Run the market research crew.")
    parser.add_argument(
        "market_segment",
        nargs="?",
        default="Sustainable Technologies",
        help="Market segment to research (default: 'Sustainable Technologies').",
    )
    args = parser.parse_args(argv)

    check_environment()

    crew = build_market_research_crew()
    result = crew.kickoff(inputs={"market_segment": args.market_segment})

    print("\n=== RESEARCH REPORT ===\n")
    print(result)


if __name__ == "__main__":
    main(sys.argv[1:])
