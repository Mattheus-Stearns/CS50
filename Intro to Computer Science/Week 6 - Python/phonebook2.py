import csv

def get_str(text: str) -> str: # Cannot handle not having a positional argument
    try:
        s = str(input(text))
    except ValueError:
        return get_str(text)
    else:
        return s

name = get_str("Name: ")
number = get_str("Number: ")

with open("phonebook.csv", "a") as file:

    writer = csv.DictWriter(file, fieldnames=["name, number"])
    writer.writerow({"name": name, "number": number})
