def count_frequencies(numbers):
    count = dict()
    
    for number in numbers:
        if number in count:
            count[number] += 1
        else:
            count[number] = 1
    return count

if __name__ == "__main__":
    frequency = count_frequencies([1,2,2,3,1,2])
    print(frequency)