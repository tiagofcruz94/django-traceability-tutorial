from decimal import Decimal

value = Decimal("60.0")

a = f"{value:.1f}"
b = {f"{value:.1f}"}

print(a)
print(type(a))
print(b)
print(type(b))


def yield_display(carcass_yield):
    return f"{carcass_yield:.1f}"


print(type(yield_display(value)))
