def find_first_duplicate(numbers):
    seen = set()
    for number in numbers:
        if number in seen:
            return number
        else:
            seen.add(number)

    return None

if __name__ == "__main__":
    print(find_first_duplicate([7,3,7,2,3]))