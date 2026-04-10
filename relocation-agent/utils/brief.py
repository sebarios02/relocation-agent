from fpdf import FPDF
import datetime

def clean(text: str) -> str:
    replacements = {
        "\u2013": "-", "\u2014": "-", "\u2018": "'", "\u2019": "'",
        "\u201c": '"', "\u201d": '"', "\u2026": "...", "\u2022": "-",
        "\u20ac": "EUR", "\u00e9": "e", "\u00e8": "e", "\u00ea": "e",
        "\u00e0": "a", "\u00e1": "a", "\u00e2": "a", "\u00f3": "o",
        "\u00f2": "o", "\u00fa": "u", "\u00fc": "u", "\u00f1": "n",
        "\u00e7": "c", "\u00b2": "2", "\u00b0": " degrees",
        "\u00ef": "i", "\u00ee": "i", "\u00e4": "a", "\u00f6": "o",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    # Remove any remaining non-latin characters
    return text.encode("latin-1", errors="replace").decode("latin-1")

def safe_cell(pdf, text):
    try:
        cleaned = clean(str(text))
        # Force encode/decode to strip anything problematic
        cleaned = cleaned.encode("ascii", errors="ignore").decode("ascii")
        if cleaned.strip():
            pdf.multi_cell(0, 6, cleaned)
    except Exception:
        pass

def generate_brief(profile: dict, top_matches: list, recommendation: str, lifestyle: list = None) -> str:
    pdf = FPDF()
    pdf.set_margins(15, 15, 15)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 10, "Relocation Brief - Barcelona", ln=True, align="C")
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 7, f"Generated: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align="C")
    pdf.ln(6)

    # Profile
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Your Profile", ln=True)
    pdf.set_font("Helvetica", "", 10)
    for key, value in profile.items():
        safe_cell(pdf, f"{key.capitalize()}: {value}")
    pdf.ln(4)

    # Top neighborhoods
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Top Recommended Neighborhoods", ln=True)
    for match in top_matches:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 7, clean(f"{match['zone']} - Score: {match['score']}/100"), ln=True)
        pdf.set_font("Helvetica", "", 10)
        safe_cell(pdf, match.get("summary", ""))
        if match.get("listings"):
            for listing in match["listings"][:2]:
                safe_cell(pdf, f"- {listing['title']} | {listing['price']}EUR/mo | {listing['sqm']}sqm")
        pdf.ln(2)

    # Lifestyle
    if lifestyle:
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 8, "Your Lifestyle Guide", ln=True)
        for area in lifestyle:
            pdf.set_font("Helvetica", "B", 11)
            pdf.cell(0, 7, clean(area.get("zone", "")), ln=True)
            pdf.set_font("Helvetica", "", 10)
            gyms = ", ".join(area.get("gyms", []))
            restaurants = ", ".join(area.get("restaurants", []))
            activities = ", ".join(area.get("activities", []))
            safe_cell(pdf, f"Gyms: {gyms}")
            safe_cell(pdf, f"Restaurants: {restaurants}")
            safe_cell(pdf, f"Activities: {activities}")
            if area.get("hidden_gems"):
                safe_cell(pdf, f"Insider tip: {area['hidden_gems']}")
            pdf.ln(2)

    # Recommendation
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Personalized Recommendation", ln=True)
    pdf.set_font("Helvetica", "", 10)
    safe_cell(pdf, recommendation)

    path = "/tmp/relocation_brief.pdf"
    pdf.output(path)
    return path