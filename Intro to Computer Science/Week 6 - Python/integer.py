def get_int(text: str) -> int:
    try:
        n = int(input(text))
    except ValueError:
        return get_int(text)
    else:
        return n
    
n = get_int("Integer: ")
print(f"Twice the integer is: {n * 2}")