from fastapi import FastAPI
from pydantic import BaseModel
import os
from crewai import Agent, Task, Crew, LLM
from litellm import RateLimitError

os.environ["GROQ_API_KEY"] = "your_real_groq_key"

llm = LLM(model="groq/llama-3.1-8b-instant", temperature=0.4, max_tokens=500)
app = FastAPI()

class DecisionInput(BaseModel):
    decision: str
    income: str
    savings: str
    dependents: str

@app.post("/analyze")
def analyze(input: DecisionInput):
    user_context = f"""
    Decision: {input.decision}
    Monthly Income: {input.income}
    Savings: {input.savings}
    Dependents: {input.dependents}
    """

    profile_agent = Agent(role="Profile Analyst", goal="Analyze user", llm=llm, verbose=False)
    market_agent = Agent(role="Market Analyst", goal="Analyze market", llm=llm, verbose=False)
    financial_agent = Agent(role="Financial Analyst", goal="Analyze finance", llm=llm, verbose=False)
    final_agent = Agent(role="Final Decision", goal="Combine insights", llm=llm, verbose=False)

    task1 = Task(description=f"Profile analysis: {user_context}", agent=profile_agent)
    task2 = Task(description=f"Market analysis: {input.decision}", agent=market_agent)
    task3 = Task(description=f"Financial analysis: {user_context}", agent=financial_agent)
    task4 = Task(description="Final decision", agent=final_agent)

    crew = Crew(agents=[profile_agent, market_agent, financial_agent, final_agent],
                tasks=[task1, task2, task3, task4])

    try:
        result = crew.kickoff()
        return {"result": result}
    except RateLimitError:
        return {"error": "API rate limit reached"}
    except Exception as e:
        return {"error": str(e)}
