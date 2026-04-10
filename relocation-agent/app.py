import streamlit as st
import os
import time
from langchain_anthropic import ChatAnthropic
from rag.neighborhoods import get_retriever
from agents.profiler import PROFILE_QUESTIONS, build_profile_from_answers, infer_hidden_preferences
from agents.neighborhood import score_neighborhood
from agents.match import get_top_matches, enrich_with_listings, generate_recommendation, generate_lifestyle_guide
from utils.brief import generate_brief

st.set_page_config(page_title="Relocation Agent BCN", page_icon="🏙️", layout="centered")

api_key = st.secrets["ANTHROPIC_API_KEY"]
os.environ["ANTHROPIC_API_KEY"] = api_key

st.title("🏙️ Relocation Agent Barcelona")
st.caption("Your smart assistant to find the perfect neighborhood in Barcelona")

if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.answers = {}
    st.session_state.profile_text = ""
    st.session_state.scores = []
    st.session_state.top_matches = []
    st.session_state.recommendation = ""
    st.session_state.lifestyle = []

llm = ChatAnthropic(model="claude-sonnet-4-20250514", temperature=0.3, api_key=api_key)

ZONE_COORDS = {
    "Eixample": [41.3874, 2.1686],
    "Les Corts": [41.3837, 2.1317],
    "Sant Martí": [41.4116, 2.2050],
    "Gràcia": [41.4036, 2.1534],
    "Sarrià - Sant Gervasi": [41.4023, 2.1234],
    "Ciutat Vella": [41.3826, 2.1769],
}

IDEALISTA_URLS = {
    "Eixample": "https://www.google.com/search?q=alquiler+piso+Eixample+Barcelona+idealista",
    "Les Corts": "https://www.google.com/search?q=alquiler+piso+Les+Corts+Barcelona+idealista",
    "Sant Martí": "https://www.google.com/search?q=alquiler+piso+Sant+Marti+Barcelona+idealista",
    "Gràcia": "https://www.google.com/search?q=alquiler+piso+Gracia+Barcelona+idealista",
    "Sarrià - Sant Gervasi": "https://www.google.com/search?q=alquiler+piso+Sarria+Sant+Gervasi+Barcelona+idealista",
    "Ciutat Vella": "https://www.google.com/search?q=alquiler+piso+Ciutat+Vella+Barcelona+idealista",
}

# STEP 1: Profile questions
if st.session_state.step < len(PROFILE_QUESTIONS):
    current_q = PROFILE_QUESTIONS[st.session_state.step]
    st.progress((st.session_state.step) / len(PROFILE_QUESTIONS))
    st.subheader(f"Question {st.session_state.step + 1} of {len(PROFILE_QUESTIONS)}")
    st.markdown(f"### {current_q['question']}")

    answer = None

    if current_q["type"] == "select":
        answer = st.radio(
            label=current_q["question"],
            options=current_q["options"],
            label_visibility="collapsed"
        )

    elif current_q["type"] == "select_or_other":
        options_with_other = current_q["options"] + ["Other"]
        selected = st.radio(
            label=current_q["question"],
            options=options_with_other,
            label_visibility="collapsed"
        )
        if selected == "Other":
            other_text = st.text_input("Please specify:")
            answer = other_text.strip() if other_text.strip() else None
        else:
            answer = selected

    elif current_q["type"] == "multiselect":
        selected = st.multiselect(
            label=current_q["question"],
            options=current_q["options"],
            label_visibility="collapsed"
        )
        answer = ", ".join(selected) if selected else None

    elif current_q["type"] == "multiselect_or_other":
        options_with_other = current_q["options"] + ["Other"]
        selected = st.multiselect(
            label=current_q["question"],
            options=options_with_other,
            label_visibility="collapsed"
        )
        if "Other" in selected:
            other_text = st.text_input("Please specify:")
            selected = [s for s in selected if s != "Other"]
            if other_text.strip():
                selected.append(other_text.strip())
        answer = ", ".join(selected) if selected else None

    elif current_q["type"] == "map":
        from streamlit_folium import st_folium
        import folium

        m = folium.Map(location=[41.3874, 2.1686], zoom_start=13)
        for zone, coords in ZONE_COORDS.items():
            folium.Marker(
                location=coords,
                popup=folium.Popup(zone, max_width=200),
                tooltip=zone,
                icon=folium.Icon(color="blue", icon="home")
            ).add_to(m)

        st.caption("📍 Explore the map to see each neighborhood, then select yours below.")
        st_folium(m, width=700, height=380)

        zone_options = list(ZONE_COORDS.keys()) + ["Other / Not sure yet"]
        selected_zone = st.radio("Select your work or study area:", zone_options)
        if selected_zone == "Other / Not sure yet":
            other_text = st.text_input("Please specify:")
            answer = other_text.strip() if other_text.strip() else "Not sure yet"
        else:
            answer = selected_zone

    if st.button("Next →"):
        if answer:
            st.session_state.answers[current_q["key"]] = answer
            st.session_state.step += 1
            st.rerun()
        else:
            st.warning("Please answer before continuing.")

# STEP 2: Analysis
elif st.session_state.step == len(PROFILE_QUESTIONS):
    st.success("✅ Profile complete. Analyzing your Barcelona match...")
    with st.spinner("Agents are working on your personalized report..."):
        profile_text = build_profile_from_answers(st.session_state.answers)

        for attempt in range(3):
            try:
                hidden_prefs = infer_hidden_preferences(llm, st.session_state.answers)
                retriever = get_retriever()
                docs = retriever.invoke(profile_text)
                scores = score_neighborhood(llm, profile_text, hidden_prefs, docs)
                top_matches = get_top_matches(scores, top_n=3)
                enriched = enrich_with_listings(top_matches)
                recommendation = generate_recommendation(llm, profile_text, top_matches)
                lifestyle = generate_lifestyle_guide(llm, profile_text, top_matches)

                st.session_state.profile_text = profile_text
                st.session_state.scores = scores
                st.session_state.top_matches = enriched
                st.session_state.recommendation = recommendation
                st.session_state.lifestyle = lifestyle
                st.session_state.step += 1
                st.rerun()
                break
            except Exception as e:
                if attempt < 2:
                    st.warning(f"API busy, retrying... ({attempt + 1}/3)")
                    time.sleep(5)
                else:
                    st.error(f"Error: {str(e)}. Please try again.")

# STEP 3: Results
elif st.session_state.step > len(PROFILE_QUESTIONS):

    st.subheader("🎯 Your Relocation Score")
    for match in st.session_state.top_matches:
        zone_name = match["zone"]
        with st.expander(f"📍 {zone_name} — {match['score']}/100", expanded=True):
            col1, col2, col3 = st.columns(3)
            breakdown = match.get("breakdown", {})
            col1.metric("Price", f"{breakdown.get('price', 0)}/100")
            col2.metric("Location", f"{breakdown.get('location', 0)}/100")
            col3.metric("Lifestyle", f"{breakdown.get('lifestyle', 0)}/100")
            st.info(match["summary"])

            if zone_name in ZONE_COORDS:
                from streamlit_folium import st_folium
                import folium
                coords = ZONE_COORDS[zone_name]
                m = folium.Map(location=coords, zoom_start=15)
                folium.Marker(
                    location=coords,
                    popup=zone_name,
                    tooltip=zone_name,
                    icon=folium.Icon(color="red", icon="home")
                ).add_to(m)
                st_folium(m, width=650, height=250, key=f"map_{zone_name}")

            maps_url = f"https://www.google.com/maps/search/{zone_name.replace(' ', '+')}+Barcelona"
            idealista_url = IDEALISTA_URLS.get(zone_name, "https://www.google.com/search?q=alquiler+piso+Barcelona+idealista")
            col_a, col_b = st.columns(2)
            col_a.markdown(f"[📌 Explore on Google Maps]({maps_url})")
            col_b.markdown(f"[🏠 Find rentals on Idealista]({idealista_url})")

            if match.get("listings"):
                st.markdown("**🏠 Available properties:**")
                for listing in match["listings"]:
                    st.markdown(f"- **{listing['title']}** — {listing['price']}EUR/mo | {listing['sqm']}sqm | {', '.join(listing['features'])} | [🔗 Search on Idealista]({idealista_url})")

    st.divider()
    st.subheader("🌆 Your Lifestyle Guide")
    if st.session_state.lifestyle:
        tabs = st.tabs([area["zone"] for area in st.session_state.lifestyle])
        for i, area in enumerate(st.session_state.lifestyle):
            with tabs[i]:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**🏋️ Gyms**")
                    for gym in area.get("gyms", []):
                        gym_name = gym.split(" - ")[0]
                        search_url = f"https://www.google.com/maps/search/{gym_name.replace(' ', '+')}+{area['zone'].replace(' ', '+')}+Barcelona"
                        st.markdown(f"- [{gym}]({search_url})")
                    st.markdown("**🍽️ Restaurants**")
                    for restaurant in area.get("restaurants", []):
                        rest_name = restaurant.split(" - ")[0]
                        search_url = f"https://www.google.com/maps/search/{rest_name.replace(' ', '+')}+{area['zone'].replace(' ', '+')}+Barcelona"
                        st.markdown(f"- [{restaurant}]({search_url})")
                with col2:
                    st.markdown("**🎯 Activities**")
                    for activity in area.get("activities", []):
                        act_name = activity.split(" - ")[0]
                        search_url = f"https://www.google.com/maps/search/{act_name.replace(' ', '+')}+{area['zone'].replace(' ', '+')}+Barcelona"
                        st.markdown(f"- [{activity}]({search_url})")
                    if area.get("hidden_gems"):
                        st.success(f"💎 **Insider tip:** {area['hidden_gems']}")
    else:
        st.info("Lifestyle guide unavailable. Try running again.")

    st.divider()
    st.subheader("💬 Personalized Recommendation")
    st.write(st.session_state.recommendation)

    st.divider()
    st.subheader("📄 Download your Relocation Brief")
    if st.button("Generate PDF"):
        try:
            path = generate_brief(
                st.session_state.answers,
                st.session_state.top_matches,
                st.session_state.recommendation,
                st.session_state.lifestyle
            )
            with open(path, "rb") as f:
                st.download_button("⬇️ Download Brief", f, file_name="relocation_brief.pdf", mime="application/pdf")
        except Exception as e:
            st.error(f"PDF error: {str(e)}")

    if st.button("🔄 Start over"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()