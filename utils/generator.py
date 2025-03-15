import random
import math

# Load words from a wordlist file
def load_wordlist(filename="words.txt"):
    with open(filename, "r") as f:
        return [line.split()[1] for line in f.readlines()]  # Extract second column (actual word)

# Generate a secure passphrase
import random
import string

def load_wordlist(filename="words.txt"):
    """Loads a list of words from a file."""
    with open(filename, "r") as file:
        return [word.strip() for word in file.readlines()]

def generate_passphrase(num_words=4, use_numbers=True, use_symbols=True):
    """Generates a secure passphrase with optional numbers and symbols."""
    wordlist = load_wordlist()
    words = [random.choice(wordlist).capitalize() for _ in range(num_words)]  # Capitalize words

    if use_numbers:
        words.append(str(random.randint(10, 99)))  # Adds a random 2-digit number

    if use_symbols:
        words.append(random.choice("!@#$%^&*"))  # Adds a random symbol

    random.shuffle(words)  # Shuffle for extra randomness
    return " ".join(words)


# Calculate entropy
def calculate_entropy(num_words, wordlist_size):
    return round(math.log2(wordlist_size ** num_words), 2)
