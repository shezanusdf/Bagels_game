import random

NUM_DIGITS = 3
MAX_GUESS = 10


def main():
    print(f'''Bagels, a deductive logic game.

I'm thinking of a {NUM_DIGITS}-digit number with no repeated digits.
Try to guess what it is. Here are some clues : 
When I say:    That means:
  Pico         One digit is correct but in the wrong position.
  Fermi        One digit is correct and in the right position.
  Bagels       No digits are correct.
  
  For example : if the secret number was 248 and your guess was 843,
  the clues would be Fermi Pico.''')
    
    while True: # Main game loop
        # This stores the the secret number the player needs to guess.
        secret_num = get_secret_num()
        print("I have a secret three-digit number in mind.")
        print(f"You have {MAX_GUESS} guesses to get it.")
        
        num_guesses = 1
        while num_guesses <= 10 :
            guess = ''
            # Keep looping until they enter 3 digits
            while len(guess) != NUM_DIGITS or not guess.isnumeric() :
                print(f"Guess #{num_guesses}")
                guess = input("> ")
                
            clues = getclues(guess, secret_num)
            print(clues)
            num_guesses+=1
            
            if guess == secret_num:
                print("You got it!")
                break
            if num_guesses > MAX_GUESS:
                print("You ran out of guesses.")
                print(f"The answer was {secret_num}")
        # Ask player if they want to play again.
        print("Do you want to play again? (yes or no)")
        if not input("> ").lower().startswith("y"):
            print("Thanks for playing!")
            break
        
        

def get_secret_num():
    num_list = list(range(10))
    random.shuffle(num_list)
    secret_num = ""
    
    for i in num_list [0:(NUM_DIGITS)]:
        secret_num += str(i)
        
    return secret_num

def getclues(guess, secret_num):
    clues = []
    for i in range(NUM_DIGITS) :
        if guess[i] == secret_num[i]:
            clues.append("fermi")
        for y in range(NUM_DIGITS) :
            if guess[i] == secret_num[y] and secret_num[i] != guess[i]:
                clues.append("pico")
    
    if len(clues) == 0:
        clues.append("bagels")
    clues.sort()
    return ' '.join(clues)
    
            
if __name__ == '__main__':
    main()
        
        
print(get_secret_num)