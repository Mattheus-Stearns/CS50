def get_str(text: str) -> str: # Cannot handle not having a positional argument
    try:
        s = str(input(text))
    except ValueError:
        return get_str(text)
    else:
        return s

def main():
    text = get_str("Text: ")
    L = averageNumofLetters(text)
    S = averageNumofSentences(text)
    grade = 0.0588 * L - 0.296 * S - 15.8
    index = round(grade)

    if index < 1:
        print("Before Grade 1")
    elif index >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {index}")

def numofWords(s: str) -> int:
    words = 1
    for i in range(len(s)):
        if s[i] == " ":
            words += 1
    return words

def averageNumofLetters(s: str) -> float:
    letters = 0
    for i in range(len(s)):
        if s[i].isalnum():
            letters += 1
    return 100.0 * letters / numofWords(s)

def averageNumofSentences(s: str) -> float:
    sentences = 0
    for i in range(len(s)):
        if s[i] == '.' or s[i] == '!' or s[i] == '?':
            if i + 1 < len(s):
                if s[i + 1] != '.':
                    sentences += 1
            else:
                sentences += 1
    return 100.0 * sentences / numofWords(s)

main()