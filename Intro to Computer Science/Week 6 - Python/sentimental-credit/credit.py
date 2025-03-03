def get_str(text: str) -> str: # Cannot handle not having a positional argument
    try:
        s = str(input(text))
    except ValueError:
        return get_str(text)
    else:
        return s

def main():
    n = get_str("Number: ")

    result = checksum(n)

    if result:
        print(f"{issuer(n)}")
    else:
        print("INVALID")


def checksum(n: str) -> bool:
    lengthN = len(n)
    checksum = 0

    for i in range(lengthN - 1, -1, -2):
        checksum += int(n[i])
        if i > 0:
            doubleNum = int(n[i - 1]) * 2
            checksum += doubleNum // 10 + doubleNum % 10
    
    if lengthN not in [13, 15, 16]:
        return False
    elif checksum % 10 == 0:
        return True
    else:
        return False

def issuer(n: str) -> str:
    lengthN = len(n)
    twoDigitIdentifier = int(n[0:2])
    oneDigitIdentifier = int(n[0])

    if (twoDigitIdentifier == 34 or twoDigitIdentifier == 37) and lengthN == 15:
        return "AMEX"
    elif twoDigitIdentifier > 50 and twoDigitIdentifier < 56 and lengthN == 16:
        return "MASTERCARD"
    elif oneDigitIdentifier == 4 and (lengthN == 13 or lengthN == 16):
        return "VISA"
    else:
        return "INVALID"
main()