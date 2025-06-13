from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.tools import google_search
from google.adk.tools import agent_tool

APP_NAME="google_search_agent"
USER_ID="user1234"
SESSION_ID="1234"

search_agent = Agent(
    model='gemini-2.0-flash',
    name='SearchAgent',
    instruction="""
    Takes a persons name, company and other details as input. Does online research. Prepares a report summarizing: Business interests, Online presence (LinkedIn, company website, media mentions, etc. and give his/her contact details if available).
    """,
    tools=[google_search],
)

root_agent = Agent(
    name="RootAgent",
    model="gemini-2.0-flash",
    description="Root Agent",
    tools=[agent_tool.AgentTool(agent=search_agent)],
)

session_service = InMemorySessionService()
session = session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)

# Filter results and keep top 3 results
def filter_relevant(results):
    return results[:3]  


def research_person(name, company):
    # Search query
    query = f'"{name}" {company} news'
    
    # Get results
    results = root_agent.invoke(query)
    
    # Filter results
    filtered = filter_relevant(results) if isinstance(results, list) else []
    
    # Create report
    report = f"### Research Report: {name} ({company})\n\n"
    for result in filtered:
        report += f"- {result['title']} - {result['link']}\n"
    
    return report
