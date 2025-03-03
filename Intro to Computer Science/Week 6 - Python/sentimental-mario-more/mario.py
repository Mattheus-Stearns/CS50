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

row = 0
while row < height:
    space = 0
    while space < height - row - 1:
        print(" ", end="")
        space += 1
    
    col = 0
    while col <= row:
        print("#", end="")
        col += 1
    
    print("  ", end="")

    col = 0
    while col <= row:
        print("#", end="")
        col += 1
    
    print()
    row += 1

