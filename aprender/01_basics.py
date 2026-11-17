animal_id = "PT12345"
breed = "Angus"
weight = 600
sex = "M"

print(f"ID do animal: {animal_id}")
print(f"Raça: {breed}")
print(f"Peso: {weight}")
print(f"Sexo: {sex}")

if weight < 400:
    print("O animal é leve.")
elif weight <= 600:
    print("O animal é normal.")
else:
    print("O animal é pesado.")

if sex == "M":
    print("O animal é macho.")
else:
    print("O animal é fêmea.")
