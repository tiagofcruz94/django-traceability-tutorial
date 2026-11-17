animal_id = "PT12345"
breed = "Angus"
weight = 600
sex = "M"

print(f"Animal ID: {animal_id}")
print(f"Breed: {breed}")
print(f"Weight: {weight}")
print(f"Sex: {sex}")

if weight < 400:
    print("The animal is light.")
elif weight <= 600:
    print("The animal is normal.")
else:
    print("The animal is heavy.")

if sex == "M":
    print("The animal is male.")
else:
    print("The animal is female.")
