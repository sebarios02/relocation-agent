LISTINGS = {
    "Eixample": [
        {"id": 1, "title": "Bright apartment in Eixample Dreta", "price": 1450, "rooms": 2, "sqm": 70, "features": ["elevator", "balcony", "furnished"]},
        {"id": 2, "title": "Modern studio near Passeig de Gracia", "price": 1200, "rooms": 1, "sqm": 45, "features": ["furnished", "AC", "concierge"]},
    ],
    "Les Corts": [
        {"id": 3, "title": "Family apartment near Camp Nou", "price": 1300, "rooms": 3, "sqm": 85, "features": ["parking", "furnished", "quiet street"]},
        {"id": 4, "title": "Modern flat near Diagonal", "price": 1150, "rooms": 2, "sqm": 60, "features": ["AC", "elevator", "bright"]},
    ],
    "Sant Martí": [
        {"id": 5, "title": "Industrial loft in Poblenou", "price": 1100, "rooms": 1, "sqm": 55, "features": ["design", "tech district", "bike included"]},
        {"id": 6, "title": "New apartment near the beach", "price": 1300, "rooms": 2, "sqm": 65, "features": ["new build", "AC", "optional parking"]},
        {"id": 7, "title": "Family apartment in Diagonal Mar", "price": 1400, "rooms": 3, "sqm": 90, "features": ["sea views", "pool", "parking"]},
    ],
    "Gràcia": [
        {"id": 8, "title": "Charming flat in Vila de Gracia", "price": 1050, "rooms": 2, "sqm": 60, "features": ["terrace", "furnished", "bright"]},
        {"id": 9, "title": "Room in shared flat Gracia", "price": 650, "rooms": 1, "sqm": 18, "features": ["bills included", "WiFi", "student area"]},
    ],
    "Sarrià - Sant Gervasi": [
        {"id": 10, "title": "Family flat in Sarria", "price": 1800, "rooms": 3, "sqm": 110, "features": ["garden", "parking", "school nearby"]},
        {"id": 11, "title": "Executive flat in Sant Gervasi", "price": 1600, "rooms": 2, "sqm": 85, "features": ["views", "24h concierge", "gym"]},
    ],
    "Ciutat Vella": [
        {"id": 12, "title": "Historic flat in Gothic Quarter", "price": 1350, "rooms": 2, "sqm": 55, "features": ["high ceilings", "central", "furnished"]},
        {"id": 13, "title": "Renovated studio in El Born", "price": 1150, "rooms": 1, "sqm": 42, "features": ["furnished", "bright", "trendy area"]},
    ],
}

def get_listings_for_zone(zone: str):
    return LISTINGS.get(zone, [])