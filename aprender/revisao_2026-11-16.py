from decimal import Decimal

valor = "60,0"

a = valor
b = {valor}
c = f"{valor}"

print(a)
print(b)
print(c)

print(type(a))
print(type(b))
print(type(c))

d = "False" or Decimal("0")

print(d)
