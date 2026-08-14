def get_numbers():
    numbers = []
    for i in range(5):
        numbers.append(int(input(f"number {i}: ")))
    return numbers

def analyze_numbers(numbers):
    largest = numbers[0]
    smallest = numbers[0]
    total = 0
    even = 0
    odd = 0
    for number in numbers:
        total += number
        if number > largest:
            largest = number
        if number < smallest:
            smallest = number
        if number % 2 == 0:
            even += 1
        else:
            odd += 1
    return(largest, smallest, total, even, odd)
   

if __name__ == "__main__":
    numbers = get_numbers()
    largest, smallest, total, even, odd, n =analyze_numbers(numbers)
    print("largest: ", largest)
    print("smallest: ", smallest)
    print("average: ", total/len(numbers))
    print("Even numbers: ", even)
    print("Odd numbers: ", odd)
    

