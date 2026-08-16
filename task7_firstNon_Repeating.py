def first_unique_char(Text):
    count = dict()
    for char in Text:
        if char in count:
            count[char] += 1
        else:
            count[char] = 1

    for c, f in count.items():
        if f == 1:
            return c
    return None

if __name__ == "__main__":
    print(first_unique_char("swiss"))
    print(first_unique_char("aabbcc"))
