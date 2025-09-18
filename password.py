import re
import math

# Common weak passwords (can be extended or loaded from a file)
COMMON_PASSWORDS = ["123456", "password", "123456789", "qwerty", "letmein", "welcome"]

def calculate_entropy(password):
    """Calculate password entropy in bits."""
    pool_size = 0
    if re.search(r"[a-z]", password): pool_size += 26
    if re.search(r"[A-Z]", password): pool_size += 26
    if re.search(r"[0-9]", password): pool_size += 10
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): pool_size += 32
    return len(password) * math.log2(pool_size) if pool_size else 0

def check_password_strength(password):
    score = 0
    feedback = []

    # Length
    if len(password) >= 12:
        score += 30
    elif len(password) >= 8:
        score += 20
    else:
        feedback.append("Make your password at least 8 characters long.")

    # Uppercase & Lowercase
    if re.search(r"[a-z]", password) and re.search(r"[A-Z]", password):
        score += 20
    else:
        feedback.append("Use both uppercase and lowercase letters.")

    # Numbers
    if re.search(r"[0-9]", password):
        score += 20
    else:
        feedback.append("Add some numbers.")

    # Special Characters
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 20
    else:
        feedback.append("Add some special characters (e.g. @, #, $, %).")

    # Check common passwords
    if password.lower() in COMMON_PASSWORDS:
        feedback.append("This is a common password! Change it immediately.")
        score = min(score, 30)  # downgrade score

    # Entropy
    entropy = calculate_entropy(password)
    if entropy >= 60:
        score += 10
    else:
        feedback.append("Increase password complexity to raise entropy.")

    # Cap score at 100
    score = min(score, 100)

    # Strength Level
    if score >= 80:
        strength = "Very Strong 💪"
    elif score >= 60:
        strength = "Strong 🙂"
    elif score >= 40:
        strength = "Medium 😐"
    else:
        strength = "Weak ❌"

    return {
        "password": password,
        "score": score,
        "entropy_bits": round(entropy, 2),
        "strength": strength,
        "suggestions": feedback if feedback else ["Great job! Your password is strong."]
    }

# Example usage
if __name__ == "__main__":
    pw = input("Enter a password to test: ")
    result = check_password_strength(pw)

    print(f"\nPassword: {result['password']}")
    print(f"Score: {result['score']} / 100")
    print(f"Entropy: {result['entropy_bits']} bits")
    print(f"Strength: {result['strength']}")
    print("Suggestions:")
    for f in result['suggestions']:
        print(" -", f)
