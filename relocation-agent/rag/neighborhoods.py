from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

NEIGHBORHOODS = [
    Document(
        page_content="""
        Eixample: Central and upscale neighborhood in Barcelona.
        Average rent: 1200-1800EUR/month for 1-2 bedrooms.
        Vibe: Cosmopolitan, calm, extremely well connected.
        Metro: L2, L3, L4, L5. Under 20 min from anywhere.
        Ideal for: Professionals, couples, relocated executives.
        Expat community: High. Many English-speaking services.
        Nightlife: Moderate. Quality bars and restaurants.
        Downsides: Expensive, little green space, touristy in some areas.
        Documentation: Usually requires Spanish payslip or 3 months deposit.
        Gyms: Holmes Place, DiR, Anytime Fitness nearby.
        Restaurants: Wide variety, tapas bars, sushi, Mediterranean, brunch spots.
        Activities: Yoga studios, Pilates, cultural events, rooftop bars.
        Parks: Jardins de la Universitat, Parc de l'Escorxador nearby.
        """,
        metadata={"zone": "Eixample", "avg_price": 1500, "vibe": "cosmopolitan"}
    ),
    Document(
        page_content="""
        Les Corts: Quiet and well-connected residential neighborhood.
        Average rent: 1100-1600EUR/month for 1-2 bedrooms.
        Vibe: Calm, family-friendly, upscale but not flashy.
        Metro: L3, L5. Easy access to the city center and Diagonal.
        Ideal for: Families, professionals working near Diagonal, FC Barcelona fans.
        Expat community: Medium-high. Many international families.
        Nightlife: Low. Very residential area.
        Downsides: Less vibrant street life, fewer young people.
        Documentation: Formal market, good guarantees required.
        Gyms: FC Barcelona sports facilities nearby, DiR, local fitness centers.
        Restaurants: Quality local restaurants, family-friendly spots, market cuisine.
        Activities: Camp Nou visits, Parc de Cervantes, cycling routes, tennis clubs.
        Parks: Parc de Cervantes, Jardins de Can Mantega.
        """,
        metadata={"zone": "Les Corts", "avg_price": 1350, "vibe": "residential-family"}
    ),
    Document(
        page_content="""
        Sant Marti: Dynamic coastal district including Poblenou and the 22@ tech hub.
        Average rent: 900-1400EUR/month for 1-2 bedrooms.
        Vibe: Modern, creative, mix of industrial heritage and new development, beachside.
        Metro: L4. Direct access to the beach and the tech district.
        Ideal for: Tech workers, startups, young professionals, beach lovers, families.
        Expat community: High and growing. Many digital nomads and international professionals.
        Nightlife: Growing scene. Trendy bars, rooftops, beach clubs.
        Downsides: Uneven development across sub-neighborhoods, some areas still transitioning.
        Documentation: Varies widely, new buildings have stricter requirements.
        Gyms: Functional fitness studios, beach volleyball courts, open-air gym on the beach.
        Restaurants: Hipster cafes, fusion cuisine, seafood, food trucks, healthy bowls.
        Activities: Beach running, kitesurfing, coworking spaces, startup events, paddleboarding.
        Parks: Rambla del Poblenou, Parc de la Ciutadella, Parc del Forum.
        """,
        metadata={"zone": "Sant Martí", "avg_price": 1150, "vibe": "tech-creative-coastal"}
    ),
    Document(
        page_content="""
        Gracia: Bohemian and characterful neighborhood with strong local identity.
        Average rent: 900-1400EUR/month for 1-2 bedrooms.
        Vibe: Artistic, calm, tight-knit community, lots of local spots.
        Metro: L3, L4, FGC. Well connected to the center.
        Ideal for: Postgrad students, creatives, freelancers, young families.
        Expat community: Very high. Popular with Europeans and Americans.
        Nightlife: Lively but relaxed. Squares and terraces.
        Downsides: Small apartments, rising prices, little parking.
        Documentation: More flexible, many private landlords.
        Gyms: Local boutique gyms, CrossFit boxes, outdoor workout areas.
        Restaurants: Organic cafes, vegan spots, international cuisine, local tapas.
        Activities: Salsa dancing, art workshops, street festivals, flea markets.
        Parks: Park Guell walking distance, Jardins de la Tamarita nearby.
        """,
        metadata={"zone": "Gràcia", "avg_price": 1100, "vibe": "bohemian"}
    ),
    Document(
        page_content="""
        Sarria - Sant Gervasi: Upscale residential area in the upper part of the city.
        Average rent: 1300-2200EUR/month for 1-2 bedrooms.
        Vibe: Exclusive, calm, green, family-oriented.
        Metro: FGC, L6, L7. Further from the center.
        Ideal for: Executives, families with children, senior professionals.
        Expat community: High, especially corporate families.
        Nightlife: Low. Very residential.
        Downsides: Expensive, far from center, need own transport.
        Documentation: Formal market, strong guarantees required.
        Gyms: Premium clubs, tennis courts, padel, golf nearby.
        Restaurants: Fine dining, international cuisine, family restaurants, organic markets.
        Activities: Hiking in Collserola, private clubs, international schools, wine tastings.
        Parks: Parc de Collserola, Jardins de Laribal.
        """,
        metadata={"zone": "Sarrià - Sant Gervasi", "avg_price": 1700, "vibe": "exclusive-family"}
    ),
    Document(
        page_content="""
        Ciutat Vella: The historic heart of Barcelona including the Gothic Quarter and El Born.
        Average rent: 1100-1700EUR/month for 1-2 bedrooms.
        Vibe: Historic, vibrant, extremely international, never sleeps.
        Metro: L3, L4, L1. Central location with excellent connections.
        Ideal for: International students, young professionals, culture lovers, short stays.
        Expat community: Very high. Most international area in the city.
        Nightlife: Very high. Bars, clubs, terraces until very late every night.
        Downsides: Very touristy, noisy, small and often overpriced apartments, crowded streets.
        Documentation: Competitive and fast-moving market, act quickly on good listings.
        Gyms: Boutique fitness studios, yoga centers, municipal sports centers.
        Restaurants: Tapas bars, pintxos, international cuisine, rooftop restaurants, food markets.
        Activities: Museum visits, Gothic Quarter walks, flamenco shows, art galleries, food tours.
        Parks: Parc de la Ciutadella walking distance, waterfront promenade.
        """,
        metadata={"zone": "Ciutat Vella", "avg_price": 1400, "vibe": "historic-vibrant"}
    ),
]

def get_retriever():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(NEIGHBORHOODS, embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 3})