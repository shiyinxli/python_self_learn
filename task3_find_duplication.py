def find_first_duplicate(numbers):
    for i in range(0,len(numbers)):
        number1 = numbers[i]
        for j in range(i+1, len(numbers)):
            number2 = numbers[j]
            if number1 == number2:
                return number1
    return None
            

if __name__ == "__main__":
    print(find_first_duplicate([3,5,2,5,7]))

