def most_frequent(numbers):
    count = dict()
    
    for number in numbers:
        if number in count:
            count[number] += 1
        else:
            count[number] = 1

    highest_frequency = 0

    if count == {}:
        return None
    
    for n, f in count.items():
        if f > highest_frequency:
            highest_frequency = f
            most_frequent_number = n

    return most_frequent_number

        

if __name__ == "__main__":
    print(most_frequent([4,7,4,7,9]))
    print(most_frequent([5, 5, 2, 2, 2, 5]))
    print(most_frequent([]))