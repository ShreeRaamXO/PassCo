import math
import hashlib
import requests

# Common character sets used in passwords
CHARACTER_SETS = {
    "lowercase": 26,
    "uppercase": 26,
    "digits": 10,
    "special": 32  # Includes common special characters
}

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

# Convert seconds into human-readable format
def convert_time(seconds):
    time_units = [
        (60, "minutes"),
        (60, "hours"),
        (24, "days"),
        (365, "years"),
        (1_000, "millennia"),
        (1_000_000, "million years"),
        (1_000_000_000, "billion years"),
        # pointless stuff 
        # (4_500_000_000, "time since Earth formed"),
        # (13_800_000_000, "time since the Big Bang"),
        (1_000_000_000_000, "trillion years"),
        (1_000_000_000_000_000, "quadrillion years"),
        (1_000_000_000_000_000_000, "quintillion years"),
        (1_000_000_000_000_000_000_000, "sextillion years"),
        (1_000_000_000_000_000_000_000_000, "septillion years"),
        (1_000_000_000_000_000_000_000_000_000, "octillion years"),
        (1_000_000_000_000_000_000_000_000_000_000, "nonillion years"),
        (1_000_000_000_000_000_000_000_000_000_000_000, "decillion years"),
        (1_000_000_000_000_000_000_000_000_000_000_000_000, "googol years")
    ]

    for unit_value, unit_name in time_units:
        if seconds < unit_value:
            return f"{seconds:.2f} {unit_name}"
        seconds /= unit_value  # Convert to next larger unit

    return f"{seconds:.2f} googol years (basically forever!)"



# Calculate entropy for any given password
def calculate_password_entropy(password):
    charset_size = 0
    if any(c.islower() for c in password):
        charset_size += CHARACTER_SETS["lowercase"]
    if any(c.isupper() for c in password):
        charset_size += CHARACTER_SETS["uppercase"]
    if any(c.isdigit() for c in password):
        charset_size += CHARACTER_SETS["digits"]
    if any(not c.isalnum() for c in password):
        charset_size += CHARACTER_SETS["special"]

    entropy = math.log2(charset_size ** len(password)) if charset_size > 0 else 0
    return round(entropy, 2)

# Check if password is leaked using Have I Been Pwned
def check_pwned(password):
    sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1_hash[:5], sha1_hash[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)

    hashes = (line.split(":") for line in response.text.splitlines())
    if any(suffix == h for h, _ in hashes):
        return "⚠️ WARNING: This password has been found in a data breach!"
    else:
        return "✅ Safe: This password is unique!"
