SUGGESTIONS = {
    "car": {
        "impact": (
            "Car travel is one of the leading sources of personal carbon emissions. "
            "Burning petrol or diesel releases CO₂ and other pollutants that contribute "
            "to climate change, air pollution, and respiratory health issues."
        ),
        "tips": [
            {"icon": "🚌", "text": "Use public transportation (bus, metro) whenever possible."},
            {"icon": "🚗", "text": "Try carpooling with friends or colleagues to share emissions."},
            {"icon": "🚶", "text": "Walk or cycle for short distances under 3 km."},
            {"icon": "📅", "text": "Plan trips efficiently to avoid unnecessary journeys."},
            {"icon": "🔧", "text": "Maintain your vehicle regularly for better fuel efficiency."},
            {"icon": "⚡", "text": "Consider switching to an electric or hybrid vehicle."},
        ]
    },
    "petrol": {
        "impact": (
            "Burning petrol releases approximately 2.31 kg of CO₂ per litre. "
            "Petrol combustion also emits nitrogen oxides and particulate matter, "
            "contributing to urban air pollution and global warming."
        ),
        "tips": [
            {"icon": "🛣️", "text": "Avoid unnecessary vehicle trips — combine errands into one trip."},
            {"icon": "🚌", "text": "Use public transportation or carpooling for daily commutes."},
            {"icon": "🔧", "text": "Service your vehicle regularly to improve fuel efficiency."},
            {"icon": "🏎️", "text": "Maintain correct tyre pressure to reduce fuel consumption."},
            {"icon": "🚀", "text": "Avoid aggressive acceleration and braking — drive smoothly."},
            {"icon": "⚡", "text": "Consider switching to an electric or CNG vehicle."},
        ]
    },
    "diesel": {
        "impact": (
            "Diesel combustion emits approximately 2.68 kg of CO₂ per litre, "
            "slightly more than petrol. Diesel vehicles also release particulate matter "
            "which is harmful to human health and contributes to air pollution."
        ),
        "tips": [
            {"icon": "🛣️", "text": "Reduce unnecessary travel and combine multiple trips."},
            {"icon": "🚌", "text": "Prefer public transport or shared vehicles for long distances."},
            {"icon": "🔧", "text": "Regular vehicle servicing ensures optimal fuel efficiency."},
            {"icon": "🏎️", "text": "Keep tyre pressure correct to save fuel."},
            {"icon": "🚀", "text": "Drive at moderate speeds — high speeds consume more fuel."},
            {"icon": "⚡", "text": "Explore electric or hybrid alternatives for your next vehicle."},
        ]
    },
    "electricity": {
        "impact": (
            "Electricity generation from fossil fuels emits approximately 0.82 kg CO₂ "
            "per kWh. Excessive electricity use increases demand on power plants, "
            "leading to more greenhouse gas emissions and strain on the energy grid."
        ),
        "tips": [
            {"icon": "💡", "text": "Switch off lights, fans, and appliances when not in use."},
            {"icon": "🔆", "text": "Replace traditional bulbs with energy-efficient LED lights."},
            {"icon": "🌡️", "text": "Use air conditioning and heaters at optimal temperatures."},
            {"icon": "☀️", "text": "Consider installing solar panels for renewable energy."},
            {"icon": "🔌", "text": "Unplug chargers and devices in standby mode."},
            {"icon": "🏠", "text": "Use energy-efficient appliances with high star ratings."},
        ]
    },
    "bus": {
        "impact": (
            "Buses emit around 0.08 kg CO₂ per km per passenger — much lower than "
            "private cars. Using buses is already an eco-friendly choice, but there "
            "are still ways to further reduce your carbon footprint."
        ),
        "tips": [
            {"icon": "✅", "text": "Great choice! Buses are much greener than private cars."},
            {"icon": "🚶", "text": "Walk or cycle for very short distances instead of taking a bus."},
            {"icon": "🚇", "text": "Metro or electric trains are even more eco-friendly options."},
            {"icon": "🗓️", "text": "Plan trips to avoid peak hours and reduce overall travel."},
            {"icon": "🌱", "text": "Encourage friends and family to use public transport too."},
        ]
    },
    "train": {
        "impact": (
            "Trains emit approximately 0.04 kg CO₂ per km per passenger — one of the "
            "lowest carbon modes of transport. Choosing trains over cars or flights "
            "significantly reduces your carbon footprint."
        ),
        "tips": [
            {"icon": "✅", "text": "Excellent! Train travel is one of the greenest transport options."},
            {"icon": "🚇", "text": "Electric trains are even more eco-friendly than diesel trains."},
            {"icon": "🚶", "text": "Walk or cycle for the first/last mile of your journey."},
            {"icon": "🌱", "text": "Offset remaining emissions by supporting green energy projects."},
            {"icon": "📣", "text": "Advocate for better public transport in your community."},
        ]
    },
}


def get_suggestions(category):
    category = category.lower()
    return SUGGESTIONS.get(category, {
        "impact": "This activity contributes to your overall carbon footprint.",
        "tips": [
            {"icon": "🌱", "text": "Try to reduce usage where possible."},
            {"icon": "♻️", "text": "Look for eco-friendly alternatives."},
        ]
    })
