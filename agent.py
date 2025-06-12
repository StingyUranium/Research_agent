from google.adk.agents import Agent
from google.adk.tools import google_search

# Initialize agent
root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='root_agent',
    description='A helpful sales research agent',
    instruction='Takes a person\'s name, company, and other details as input. Does online research (especially via Google). Prepares a report summarizing: Business interests, Online presence (LinkedIn, company website, media mentions, etc.), Recent activities or whereabouts (like conferences, deals, etc.)',
    tools=[google_search]
)

# Mock functions for now
def filter_relevant(results):
    # Add filtering logic based on your criteria
    return results[:3]  # Return top 3 for example

def get_linkedin_data(name, company):
    # Placeholder for LinkedIn data integration (API or scraping)
    return f"LinkedIn profile data for {name} at {company}"

def generate_report(name, company, search_results, linkedin_data):
    report = f"### Research Report for {name} ({company})\n\n"
    report += "**LinkedIn Data:**\n" + linkedin_data + "\n\n"
    report += "**Online Mentions:**\n"
    for result in search_results:
        report += f"- {result['title']} ({result['link']})\n"
    return report

# Final working function
def handle_person_research(name, company, location=None):
    queries = [
        f'"{name}" site:linkedin.com',
        f'"{name}" {company}',
        f'"{name}" {company} news',
        f'"{name}" interview {company}',
    ]

    all_results = []
    for query in queries:
        response = root_agent.invoke(query)  # Ask agent to use google_search
        if isinstance(response, list):
            all_results.extend(filter_relevant(response))

    linkedin_data = get_linkedin_data(name, company)
    return generate_report(name, company, all_results, linkedin_data)
