import json
import re
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from data.listings import get_listings_for_zone

def get_top_matches(scores: list, top_n: int = 3) -> list:
    sorted_scores = sorted(scores, key=lambda x: x["score"], reverse=True)
    return sorted_scores[:top_n]

def enrich_with_listings(top_zones: list) -> list:
    enriched = []
    for zone in top_zones:
        listings = get_listings_for_zone(zone["zone"])
        enriched.append({**zone, "listings": listings})
    return enriched

def generate_recommendation(llm, profile: str, top_matches: list) -> str:
    matches_text = ""
    for match in top_matches:
        matches_text += f"\n{match['zone']} (Score: {match['score']}): {match['summary']}\n"

    messages = [
        SystemMessage(content="""You are an expert relocation consultant in Barcelona.
        Your tone is warm, professional and direct — like a friend who knows Barcelona perfectly.
        Generate a personalized recommendation of maximum 200 words explaining
        why these neighborhoods are the best fit for this specific client.
        Mention concrete details from their profile to show you truly understand them."""),
        HumanMessage(content=f"""
        PROFILE: {profile}
        TOP NEIGHBORHOODS: {matches_text}

        Generate the personalized recommendation.
        """)
    ]
    response = llm.invoke(messages)
    return response.content

def generate_lifestyle_guide(llm, profile: str, top_matches: list) -> dict:
    zones = [m["zone"] for m in top_matches]
    messages = [
        SystemMessage(content="""You are a local Barcelona lifestyle expert.
        Based on the client profile and their top recommended neighborhoods,
        generate personalized lifestyle recommendations.

        Return ONLY valid JSON with this exact format, no extra text:
        {
          "lifestyle": [
            {
              "zone": "neighborhood name",
              "gyms": ["Gym 1 - brief description", "Gym 2 - brief description"],
              "restaurants": ["Restaurant 1 - cuisine type", "Restaurant 2 - cuisine type"],
              "activities": ["Activity 1 - brief description", "Activity 2 - brief description"],
              "hidden_gems": "One insider tip specific to this client's interests"
            }
          ]
        }"""),
        HumanMessage(content=f"""
        CLIENT PROFILE:
        {profile}

        TOP NEIGHBORHOODS: {', '.join(zones)}

        Generate personalized lifestyle recommendations for each neighborhood based on this client's interests and lifestyle.
        """)
    ]
    response = llm.invoke(messages)
    raw = response.content
    import re
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())["lifestyle"]
        except Exception:
            return []
        print("RAW LIFESTYLE RESPONSE:", raw)
    return []