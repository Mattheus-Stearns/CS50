def get_int(text: str) -> int:
    try:
        n = int(input(text))
    except ValueError:
        return get_int(text)
    else:
        return n

scores = []

for _ in range(3):
    score = get_int("Score: ")
    scores += [score]

average = sum(scores) / len(scores)

print(f"Average: {average:.2f}")