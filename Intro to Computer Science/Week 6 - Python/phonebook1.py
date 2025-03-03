def get_str(text: str) -> str: # Cannot handle not having a positional argument
    try:
        s = str(input(text))
    except ValueError:
        return get_str(text)
    else:
        return s

'''
people = [
    {"name": "Yulia", "number": "+1-617-495-1000"},
    {"name": "David", "number": "+1-617-495-1000"},
    {"name": "John", "number": "+1-949-468-2750"}
]

name = get_str("Name: ")
for person in people:
    if person["name"] == name:
        number = person["number"]
        print(f"Found: {number}")
        break
else:
    print("Not found.")
'''

people = {
    "Yulia": "+1-617-495-1000",
    "David": "+1-617-495-1000",
    "John": "+1-949-468-2750"
}

name = get_str("Name: ")

if name in people:
    print(f"Number: {people[name]}")
else:
    print("Not found.")
