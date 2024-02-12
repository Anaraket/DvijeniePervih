ATTEMPTS = 10
max_number = 1000
min_number = 1
count = 1

while count <= ATTEMPTS:
    my_number = (max_number + min_number) // 2
    print(my_number)
    answer = input("Больше (>) или меньше (<): ")
    if answer == ">":
        min_number = my_number
    elif answer == "<":
        max_number = my_number
    else:
        print(f"Робот угадал число за {count} попыток")
        break
    count += 1
else:
    print(f"Робот не смог угадать число даже за {ATTEMPTS} попыток")