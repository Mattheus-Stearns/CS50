def get_int(text: str) -> int: # Requires positional argument
    try:
        n = int(input(text))
    except ValueError:
        return get_int(text)
    else:
        return n

while True:
    height = get_int("Height: ")
    if height >= 1 and height <= 8:
        break

