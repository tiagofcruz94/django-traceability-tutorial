class Animal:
    def __init__(self, identification_number, breed, live_weight, sex):
        self.identification_number = identification_number
        self.breed = breed
        self.live_weight = live_weight
        self.sex = sex

    def weight_category(self):
        if self.live_weight < 400:
            return "light"
        elif self.live_weight <= 600:
            return "normal"
        else:
            return "heavy"

    def is_male(self):
        return self.sex == "M"

    # like __toString() in PHP or toString() in JavaScript
    def __str__(self):
        return f"ID: {self.identification_number}, Breed: {self.breed}, Weight: {self.live_weight} kg, Sex: {self.sex}"


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
    print(f"The animal is {animal.weight_category()}.")
    print(f"Carcass yield: {animal.carcass_yield():.1f}%\n")


avg_yield = sum(animal.carcass_yield() for animal in animals) / len(animals)
male_count = sum(1 for animal in animals if animal.is_male())

print(f"Average carcass yield: {avg_yield:.1f}%")
print(f"Number of male animals: {male_count}")
