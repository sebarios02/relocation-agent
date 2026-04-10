from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

PROFILE_QUESTIONS = [
    {
        "key": "reason",
        "question": "What is the reason for your relocation to Barcelona?",
        "type": "select_or_other",
        "options": ["Work", "Studies", "Digital nomad", "Family"]
    },
    {
        "key": "duration",
        "question": "How long are you planning to stay?",
        "type": "select_or_other",
        "options": ["Less than 3 months", "3-6 months", "6-12 months", "More than 1 year"]
    },
    {
        "key": "budget",
        "question": "What is your monthly budget for rent?",
        "type": "select_or_other",
        "options": ["Under 700EUR", "700-1000EUR", "1000-1400EUR", "1400-1800EUR", "Over 1800EUR"]
    },
    {
        "key": "companions",
        "question": "Who are you moving with?",
        "type": "select_or_other",
        "options": ["Alone", "With partner", "With family", "With friends / flatmates"]
    },
    {
        "key": "lifestyle",
        "question": "How would you describe your ideal lifestyle?",
        "type": "multiselect_or_other",
        "options": ["Quiet & calm", "Active & sporty", "Nightlife & social", "Culture & arts", "Nature & outdoors", "Foodie", "Work-focused"]
    },
    {
        "key": "work_area",
        "question": "Where will you work or study in Barcelona?",
        "type": "map",
        "options": []
    },
    {
        "key": "interests",
        "question": "What are your main hobbies and interests?",
        "type": "multiselect_or_other",
        "options": ["Gym & fitness", "Running & cycling", "Beach & water sports", "Restaurants & food", "Art & museums", "Live music & concerts", "Yoga & wellness", "Tech & startups", "Shopping"]
    },
]

def build_profile_from_answers(answers: dict) -> str:
    profile_text = "CLIENT PROFILE:\n"
    for key, value in answers.items():
        profile_text += f"- {key}: {value}\n"
    return profile_text

def infer_hidden_preferences(llm, answers: dict) -> str:
    profile_text = build_profile_from_answers(answers)
    messages = [
        SystemMessage(content="""You are a relocation expert in Barcelona with 10 years of experience.
        Analyze the client profile and infer implicit preferences they have not directly mentioned.
        For example: if they mention working in the 22@ district and enjoying sports, they probably value
        being close to the beach and modern spaces even if they haven't said so.
        Also consider their lifestyle and interests to infer what kind of neighborhood atmosphere,
        restaurants, gyms and activities would make them happiest.
        Be specific and concise. Maximum 5 inferences."""),
        HumanMessage(content=f"{profile_text}\n\nInfer the implicit preferences of this client.")
    ]
    response = llm.invoke(messages)
    return response.content