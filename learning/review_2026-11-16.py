from decimal import Decimal

value = "60,0"

a = value
b = {value}
c = f"{value}"

print(a)
print(b)
print(c)

print(type(a))
print(type(b))
print(type(c))

d = "False" or Decimal("0")

print(d)
