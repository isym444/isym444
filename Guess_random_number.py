import random
print("This is a game where you have to guess the number the computer is thinking of. You have 3 tries to guess the number. Only enter whole numbers.")
a = random.randint(1, 10)
print(a)
#e = int("2.5")
breaker = 0
while True:
    b = input("Please enter an integer between 1 and 10: ")
    try:
        b = int(b)
        if(b >= 1 and b <= 10):
            break
        else:
            raise ValueError
    except ValueError:
        print("That's not a valid integer or was outside of the required range of integers. Please try again.")
c = 2
while(b != a and c > 0):
    if(b > a):
        print(f"That was incorrect, your guess was too high, keep trying. You have {c} tries left")
    else:
        print(f"That was incorrect, your guess was too low, keep trying. You have {c} tries left")
    while True:
        b = input("Try another integer between 1 and 10: ")
        try:
            b = int(b)
            if(b >= 1 and b <= 10):
                break
            else:
                raise ValueError
        except ValueError:
            print("That's not a valid integer or was outside of the required range of integers. Please try again.")
    c -= 1
if(b == a):
    print("You guessed correctly!")
else:
    print(f"You ran out of tries. The correct answer was {a}")