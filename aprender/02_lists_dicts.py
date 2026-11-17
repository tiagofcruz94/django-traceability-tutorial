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

male_count = 0
total_weight = 0

for animal in animals:
    weight = animal["live_weight"]

    print(f"ID do animal: {animal['identification_number']}")
    print(f"Raça: {animal['breed']}")
    print(f"Peso: {weight}")

    total_weight += weight

    if weight < 400:
        print("O animal é leve.\n")
    elif weight <= 600:
        print("O animal é normal.\n")
    else:
        print("O animal é pesado.\n")

    if animal["sex"] == "M":
        male_count += 1

avg_weight = total_weight / len(animals)
print(f"\nTotal de animais: {len(animals)}")
print(f"Soma dos pesos: {total_weight} e média dos pesos: {avg_weight:.1f}")
print(f"Total de animais machos: {male_count}")
