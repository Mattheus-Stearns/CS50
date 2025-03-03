def get_str(text: str) -> str: # Cannot handle not having a positional argument
    try:
        s = str(input(text))
    except ValueError:
        return get_str(text)
    else:
        return s

names = ["Yulia", "David", "John"]

name = get_str("Name: ")

for n in names:
    if name == n:
        print("Found")
        break
else:
    print("Not Found")

if name in names:
    print("Found")
else:
    print("Not Found")