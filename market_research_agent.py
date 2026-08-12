import argparse
import os
import sys

from dotenv import load_dotenv

load_dotenv()

from crewai import Agent, Crew, Process, Task, LLM
from crewai_tools import SerperDevTool


claude_llm = LLM(
    model="anthropic/claude-sonnet-4-6",
    api_key=os.getenv("ANTHROPIC_API_KEY"),
)


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
        llm=claude_llm,
    )

    trend_analysis_task = Task(
        description=(
            "Analyze the '{market_segment}' market segment. "
            "Identify current trends, customer preferences, and potential "
            "growth opportunities. Support each finding with data."
        ),
        expected_output=(
            "A structured report containing: "
            "(1) top 3–5 current trends, "
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the market research agent.")
    parser.add_argument(
        "market_segment",
        nargs="?",
        default="Sustainable Technologies",
        help="Market segment to research (default: 'Sustainable Technologies')",
    )
    return parser.parse_args()


if __name__ == "__main__":
    required_keys = ["ANTHROPIC_API_KEY", "SERPER_API_KEY"]
    missing = [k for k in required_keys if not os.getenv(k)]
    if missing:
        print(f"Error: Missing environment variables: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)

    args = parse_args()
    crew = build_market_research_crew()
    result = crew.kickoff(inputs={"market_segment": args.market_segment})
    print("\n=== RESEARCH REPORT ===\n")
    print(result)
