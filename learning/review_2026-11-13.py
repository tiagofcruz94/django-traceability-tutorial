from decimal import Decimal

carcass_yield = Decimal("68.75")

print(f"Yield: {carcass_yield:.1f} %")  # plain Python
print(f"Yield: {carcass_yield:.2f} %")

# {{ carcass_yield|floatformat:1 }}  in a Django template
