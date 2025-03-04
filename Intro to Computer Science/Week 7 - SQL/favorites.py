import csv

with open("favorites.csv", "r") as file:
    reader = csv.DictReader(file)
    counts = {}
    for row in reader:
        favorite = row["language"]
        if favorite in counts:
            counts[favorite] += 1
        else:
            counts[favorite] = 1

for favorite in sorted(counts, key=counts.get, reverse=True):
    print(f"{favorite}: {counts[favorite]}")



"""
with open("favorites.csv", "r") as file:
    swift, cplusplus, python, otherlang = 0, 0, 0, 0
        for row in reader:
            favorite = row["language"]
            if favorite == "Python":
                python += 1
            elif favorite == "C++":
                cplusplus += 1
            elif favorite == "Swift":
                swift += 1
            else:
                otherlang += 1

print(f"C++: {cplusplus}")
print(f"Swift: {swift}")
print(f"Python: {python}")
print(f"Other language: {otherlang}")
"""