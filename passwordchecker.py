import math
import re
from getpass import getpass

# Sample dictionary of weak words (in reality, this would be a huge list)
common_words = ['password', 'admin', 'user', 'login', 'welcome', 'qwerty', 'abc123']

leet_map = {
    '0': 'o', '1': 'l', '3': 'e', '4': 'a', '5': 's', '7': 't', '@': 'a', '$': 's', '!': 'i'
}

def estimate_entropy(password):
    charset = 0
    if re.search(r'[a-z]', password):
        charset += 26
    if re.search(r'[A-Z]', password):
        charset += 26
    if re.search(r'[0-9]', password):
        charset += 10
    if re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>/?\\|`~]', password):
        charset += 32
    if re.search(r'\s', password):
        charset += 1

    entropy = math.log2(charset) * len(password) if charset > 0 else 0
    return round(entropy, 2)

def estimate_crack_time(entropy, guesses_per_second=1e10):
    time_seconds = 2 ** entropy / guesses_per_second
    return convert_time(time_seconds)

def convert_time(seconds):
    if seconds < 1:
        return "less than a second"
    elif seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        return f"{seconds / 60:.2f} minutes"
    elif seconds < 86400:
        return f"{seconds / 3600:.2f} hours"
    elif seconds < 31536000:
        return f"{seconds / 86400:.2f} days"
    else:
        return f"{seconds / 31536000:.2f} years"

def contains_common_word(password):
    pw_lower = password.lower()
    for word in common_words:
        if word in pw_lower:
            return True
    return False

def leet_substitute(password):
    return ''.join(leet_map.get(c, c) for c in password.lower())

def password_strength(password):
    entropy = estimate_entropy(password)
    crack_time = estimate_crack_time(entropy)

    common = contains_common_word(password)
    leet_pw = leet_substitute(password)
    substitutions = leet_pw != password.lower() and contains_common_word(leet_pw)

    warnings = []
    if len(password) < 8:
        warnings.append("Password is very short")
    if common:
        warnings.append("Contains common word")
    if substitutions:
        warnings.append("Contains obfuscated dictionary word")

    if entropy < 28:
        strength = "Very Weak"
    elif entropy < 36:
        strength = "Weak"
    elif entropy < 60:
        strength = "Moderate"
    elif entropy < 100:
        strength = "Strong"
    else:
        strength = "Very Strong"

    return {
        "entropy": entropy,
        "crack_time": crack_time,
        "strength": strength,
        "warnings": warnings
    }

# Test
password = getpass("Enter your password: ")
result = password_strength(password)

print("\n--- Password Analysis ---")
print(f"Entropy: {result['entropy']} bits")
print(f"Estimated Crack Time: {result['crack_time']}")
print(f"Strength: {result['strength']}")
if result['warnings']:
    print("Warnings:")
    for w in result['warnings']:
        print(f"- {w}")
