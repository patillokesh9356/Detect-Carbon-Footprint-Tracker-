EMISSION_FACTORS = {
    "electricity": 0.82,
    "petrol": 2.31,
    "diesel": 2.68,
    "car": 0.21,
    "bus": 0.08,
    "train": 0.04
}


def calculate_emission(category, value):
    category = category.lower()

    if category not in EMISSION_FACTORS:
        return None

    factor = EMISSION_FACTORS[category]
    emission = value * factor

    return round(emission, 2)