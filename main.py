import os
import argparse
from crewai import Agent, Task, Crew, LLM
from tools import SimplePriceTool, SimpleNewsTool

# 1. Environment Setup for Local Run
os.environ["OPENAI_API_KEY"] = "lm-studio" # Dummy key for LiteLLM

# 2. Pointing to Phi-4 in LM Studio
local_llm = LLM(
    model="openai/phi-4",
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)

def main():
    # 3. Setup Command Line Arguments
    parser = argparse.ArgumentParser(description="Single Stock AI Analyst")
    parser.add_argument("ticker", help="Stock ticker symbol (e.g., AARTIIND.NS)")
    args = parser.parse_args()

    # 4. Define a Single, Powerful Agent
    analyst = Agent(
        role="Stock Market Analyst",
        goal="Provide a concise 3-sentence summary for {ticker}",
        backstory=""""You are a technical swing trader. You focus on breakouts, 
        resistance levels, and volume to predict short-term price movements.""",
        tools=[SimplePriceTool(), SimpleNewsTool()],
        llm=local_llm,
        verbose=True,
        max_iter=1  # This is the "kill switch." It tells the agent it only has ONE chance to use tools.
    )

    # 5. Updated Task for Price Targeting
    analysis_task = Task(
        description="""
        STEP 1: Use the price tool to get the current LTP for {ticker}.
        STEP 2: Use the news tool to get headlines. 
        STEP 3: If a tool fails or returns an error, do NOT retry. Use the data you have.
        STEP 4: Evaluate if {ticker} can reach 514 based on technical resistance and news.
        """,
        expected_output="A final probability verdict for the 514 target.",
        agent=analyst
    )

    # 6. Assemble and Kickoff
    crew = Crew(
        agents=[analyst],
        tasks=[analysis_task],
        verbose=True
    )

    print(f"\n📈 ANALYSING: {args.ticker} ... please wait for Phi-4 to think.")
    result = crew.kickoff(inputs={'ticker': args.ticker})

    print("\n" + "="*30)
    print(f"FINAL VERDICT FOR {args.ticker}")
    print("="*30)
    print(result)

if __name__ == "__main__":
    main()
