def get_int(text: str) -> int:
    try:
        n = int(input(text))
    except ValueError:
        return get_int(text)
    else:
        return n

while True:
    n = get_int("Height: ")
    if n > 0:
        break

for _ in range(n):
    print("#")

print("?" * 4)

for i in range(3):
    print("#" * 33)