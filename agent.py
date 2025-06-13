from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.tools import google_search

APP_NAME="google_search_agent"
USER_ID="user1234"
SESSION_ID="1234"

root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='sales_researcher',
    description='Sales research agent',
    instruction='Research people and companies online',
    tools=[google_search]
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
