from decimal import Decimal

carcass_yield = Decimal("68.75")

print(f"Rendimento: {carcass_yield:.1f} %")  # python puro
print(f"Rendimento: {carcass_yield:.2f} %")

# {{ carcass_yield|floatformat:1 }} #template django
