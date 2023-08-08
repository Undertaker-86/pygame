import random



while True:
    try:
        upper_number = int(input("Level: "))

        if upper_number < 2:
            raise ValueError
        
        break
    except ValueError:
        pass

golden_fever = random.randint(1, int(upper_number))

while True:
    guess = int(input("Guess: "))

    if guess == golden_fever:
        print("Just right!")
        break

    elif guess > golden_fever:
        print("Too large!")

    else:
        print("Too small!")