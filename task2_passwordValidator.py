def validate_password(password):
    flag = False
    upper = 0
    lower = 0
    digit = 0
    special = 0
    n = 0
    for char in password:
        n += 1
        if char.isupper():
            upper += 1
        if char.islower():
            lower += 1
        if char.isdigit():
            digit += 1
        if char in ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "="]:
            special += 1

    if n>=8 and upper > 0 and lower > 0 and digit > 0 and special >0:
        flag = True

    return flag

if __name__ == "__main__":
    password = input("input your password: ")
    judge = validate_password(password)
    print(judge)

