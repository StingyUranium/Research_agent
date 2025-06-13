from google.adk.agents import Agent
from google.adk.tools import google_search

# Initialize agent
agent = Agent(
    model='gemini-2.0-flash-001',
    name='sales_researcher',
    description='Sales research agent',
    instruction='Research people and companies online',
    tools=[google_search]
)

# Filter results and keep top 3 results
def filter_relevant(results):
    return results[:3]  

# Generate report
def research_person(name, company):
    # Single search query
    query = f'"{name}" {company} news'
    
    # Get results
    results = agent.invoke(query)
    
    # Filter results
    filtered = filter_relevant(results) if isinstance(results, list) else []
    
    # Create report
    report = f"### Research Report: {name} ({company})\n\n"
    for result in filtered:
        report += f"- {result['title']} - {result['link']}\n"
    
    return report
