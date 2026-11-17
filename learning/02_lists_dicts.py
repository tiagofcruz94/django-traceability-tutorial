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

    print(f"Animal ID: {animal['identification_number']}")
    print(f"Breed: {animal['breed']}")
    print(f"Weight: {weight}")

    total_weight += weight

    if weight < 400:
        print("The animal is light.\n")
    elif weight <= 600:
        print("The animal is normal.\n")
    else:
        print("The animal is heavy.\n")

    if animal["sex"] == "M":
        male_count += 1

avg_weight = total_weight / len(animals)
print(f"\nNumber of animals: {len(animals)}")
print(f"Total weight: {total_weight}, average weight: {avg_weight:.1f}")
print(f"Number of male animals: {male_count}")
