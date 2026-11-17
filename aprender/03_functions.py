animals = [
    {
        "identification_number": "PT0001",
        "breed": "Angus",
        "live_weight": 700,
        "sex": "M",
    },
    {
        "identification_number": "PT0002",
        "breed": "Mertolenga",
        "live_weight": 450,
        "sex": "F",
    },
    {
        "identification_number": "PT0003",
        "breed": "Barrosã",
        "live_weight": 380,
        "sex": "M",
    },
    {
        "identification_number": "PT0004",
        "breed": "Wagyu",
        "live_weight": 620,
        "sex": "F",
    },
]


def weight_category(weight):
    if weight < 400:
        return "leve"
    elif weight <= 600:
        return "normal"
    else:
        return "pesado"


def format_weight(weight, unit="kg", decimals=1):
    return f"{weight:.{decimals}f} {unit}"


def average_weight(animals):
    if not animals:
        return 0
    total_weight = sum(animal["live_weight"] for animal in animals)
    return total_weight / len(animals)


for animal in animals:
    weight = animal["live_weight"]

    print(f"ID do animal: {animal['identification_number']}")
    print(f"Raça: {animal['breed']}")
    print(f"Peso: {format_weight(weight, decimals=0)}")
    print(f"O animal é {weight_category(weight)}.\n")

avg = average_weight(animals)

print(f"Peso médio: {format_weight(avg)}")
print(f"Peso médio (0 casas decimais): {format_weight(avg, decimals=0)}")
