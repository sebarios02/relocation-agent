from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
import json
import re

def score_neighborhood(llm, profile: str, hidden_prefs: str, neighborhood_docs: list) -> list:
    neighborhood_text = "\n\n".join([doc.page_content for doc in neighborhood_docs])

    messages = [
        SystemMessage(content="""You are a relocation expert in Barcelona.
        Given a client profile and neighborhood information,
        generate a Relocation Score from 0 to 100 for each neighborhood.

        Return ONLY valid JSON with this exact format, no extra text:
        {
          "scores": [
            {
              "zone": "neighborhood name",
              "score": 85,
              "breakdown": {
                "price": 80,
                "location": 90,
                "lifestyle": 85,
                "expat_community": 75,
                "process_ease": 70
              },
              "summary": "One sentence explaining why this neighborhood fits this specific client"
            }
          ]
        }"""),
        HumanMessage(content=f"""
        CLIENT PROFILE:
        {profile}

        INFERRED PREFERENCES:
        {hidden_prefs}

        NEIGHBORHOOD INFORMATION:
        {neighborhood_text}

        Generate the Relocation Score for each neighborhood in JSON format.
        """)
    ]
    response = llm.invoke(messages)
    raw = response.content
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())["scores"]
        except Exception:
            return []
    return []