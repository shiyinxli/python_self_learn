def canonical_word(word):
    res = sorted(word)
    canonical = ''.join(res)
    return canonical

def group_anagrams(words):
    dictionary = dict()
    for word in words:
        canonical = canonical_word(word)
        if canonical in dictionary:
            dictionary[canonical].append(word)
        else:
            dictionary[canonical] = [word]

    anagrams = []
    for c, w in dictionary.items():
        anagrams.append(w)

    return anagrams

if __name__ == "__main__":
    words = [
    "eat",
    "tea",
    "tan",
    "ate",
    "nat",
    "bat"
]
    print(group_anagrams(words))
