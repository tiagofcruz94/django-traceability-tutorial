class Animal:
    def __init__(self, identification_number, breed, live_weight, sex):
        self.identification_number = identification_number
        self.breed = breed
        self.live_weight = live_weight
        self.sex = sex

    def weight_category(self):
        if self.live_weight < 400:
            return "leve"
        elif self.live_weight <= 600:
            return "normal"
        else:
            return "pesado"

    def is_male(self):
        return self.sex == "M"

    # equivalente a toString() em PHP
    def __str__(self):
        return f"ID: {self.identification_number}, Raça: {self.breed}, Peso: {self.live_weight} kg, Sexo: {self.sex}"


class SlaughterAnimal(Animal):
    def __init__(self, identification_number, breed, live_weight, sex, carcass_weight):
        super().__init__(identification_number, breed, live_weight, sex)
        self.carcass_weight = carcass_weight

    def carcass_yield(self):
        if self.live_weight == 0:
            return 0
        return (self.carcass_weight / self.live_weight) * 100


animals = [
    SlaughterAnimal("PT0001", "Angus", 700, "M", 420),
    SlaughterAnimal("PT0002", "Mertolenga", 450, "F", 270),
    SlaughterAnimal("PT0003", "Barrosã", 380, "M", 210),
    SlaughterAnimal("PT0004", "Wagyu", 620, "F", 400),
]


for animal in animals:
    print(animal)
    print(f"O animal é {animal.weight_category()}.")
    print(f"Rendimento de carcaça: {animal.carcass_yield():.1f}%\n")


avg_yield = sum(animal.carcass_yield() for animal in animals) / len(animals)
male_count = sum(1 for animal in animals if animal.is_male())

print(f"Rendimento médio de carcaça: {avg_yield:.1f}%")
print(f"Quantidade de animais machos: {male_count}")
