before = str(input("Before: "))
print("After: ", end="")

for c in before:
    print(c.upper(), end="")
print()

print(f"After: {before.upper()}")