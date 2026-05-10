import random

WORDS = ["python", "hangman", "computer", "keyboard", "monitor", "elephant", "umbrella", "mountain"]

STAGES = [
    """
  -----
  |   |
      |
      |
      |
  =====""",
    """
  -----
  |   |
  O   |
      |
      |
  =====""",
    """
  -----
  |   |
  O   |
  |   |
      |
  =====""",
    """
  -----
  |   |
  O   |
 /|   |
      |
  =====""",
    """
  -----
  |   |
  O   |
 /|\  |
      |
  =====""",
    """
  -----
  |   |
  O   |
 /|\  |
 /    |
  =====""",
    """
  -----
  |   |
  O   |
 /|\  |
 / \  |
  =====""",
]

word = random.choice(WORDS)
guessed = set()
wrong = 0
max_wrong = 6

print("\n ---- HANGMAN ---- ")
print(f"Word has {len(word)} letters\n")

while True:
    print(STAGES[wrong])
    print("\n " + " ".join(c if c in guessed else "_" for c in word))
    print(f"\nWrong guesses: {wrong}/{max_wrong}")

    if all(c in guessed for c in word):
        print(f"\nYou WIN! The word was '{word}'")
        break

    if wrong == max_wrong:
        print(f"\nYou LOSE! The word was '{word}'")
        break

    guess = input("\nGuess a letter: ").lower().strip()

    if len(guess) != 1 or not guess.isalpha():
        print("Enter a single letter!")
    elif guess in guessed:
        print("Already guessed that alphabet !")
    elif guess in word:
        guessed.add(guess)
        print("Correct!")
    else:
        guessed.add(guess)
        wrong += 1
        print("Wrong!")
