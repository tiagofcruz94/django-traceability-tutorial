from datetime import date

from livestock import SlaughterAnimal

animals = [
    SlaughterAnimal("PT0001", "Angus", 700, "M", 420),
    SlaughterAnimal("PT0002", "Mertolenga", 450, "F", 270),
    SlaughterAnimal("PT0003", "Barrosã", 380, "M", 210),
]

for animal in animals:
    print(f"Carcass yield: {animal.carcass_yield():.1f}%\n")

print(date.today())
