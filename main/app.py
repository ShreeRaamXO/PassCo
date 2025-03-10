from flask import Flask, render_template, request, jsonify
import random
import math
import hashlib
import requests

app = Flask(__name__)

# Load words from a wordlist file
def load_wordlist(filename="words.txt"):
    with open(filename, "r") as f:
        return [line.split()[1] for line in f.readlines()]  # Extract second column (actual word)

# Generate a passphrase
def generate_passphrase(num_words=4, separator="-"):
    words = load_wordlist()
    passphrase = separator.join(random.choices(words, k=num_words))
    return passphrase

# Calculate entropy
def calculate_entropy(num_words, wordlist_size):
    return round(math.log2(wordlist_size ** num_words), 2)

# Estimate brute-force crack time
def estimate_crack_time(entropy):
    speeds = {
        "Personal Computer (1K guesses/sec)": 1_000,
        "Botnet Attack (1 Trillion guesses/sec)": 1_000_000_000_000,
        "Supercomputer (100 Trillion/sec)": 100_000_000_000_000
    }
    
    estimates = {}
    for attack_type, speed in speeds.items():
        seconds = (2**entropy) / speed
        estimates[attack_type] = convert_time(seconds)
    
    return estimates

# Convert seconds into human-readable time
def convert_time(seconds):
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        return f"{seconds/60:.2f} minutes"
    elif seconds < 86400:
        return f"{seconds/3600:.2f} hours"
    elif seconds < 31536000:
        return f"{seconds/86400:.2f} days"
    elif seconds < 3153600000:
        return f"{seconds/31536000:.2f} years"
    else:
        return f"{seconds/3153600000:.2f} centuries"

# Check if passphrase is leaked using Have I Been Pwned API
def check_pwned(passphrase):
    sha1_hash = hashlib.sha1(passphrase.encode()).hexdigest().upper()
    prefix, suffix = sha1_hash[:5], sha1_hash[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)

    hashes = (line.split(":") for line in response.text.splitlines())
    if any(suffix == h for h, _ in hashes):
        return "⚠️ WARNING: This passphrase has been found in a data breach!"
    else:
        return "✅ Safe: This passphrase is unique!"

@app.route("/")
def index():
    return render_template("templates\index.html")

@app.route("/generate", methods=["POST"])
def generate():
    num_words = int(request.form.get("words", 4))
    passphrase = generate_passphrase(num_words)
    entropy = calculate_entropy(num_words, len(load_wordlist()))
    crack_times = estimate_crack_time(entropy)
    pwned_status = check_pwned(passphrase)

    return jsonify({
        "passphrase": passphrase,
        "entropy": entropy,
        "crack_times": crack_times,
        "pwned_status": pwned_status
    })

if __name__ == "__main__":
    app.run(debug=True)
