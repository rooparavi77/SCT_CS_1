def caesar_cipher(text, shift, mode='encrypt'):
    result = ""

    for char in text:
        if char.isalpha():  # only shift alphabets
            shift_amount = shift if mode == 'encrypt' else -shift
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift_amount) % 26 + base)
        else:
            result += char  # keep spaces, numbers, punctuation unchanged
    return result


# Main program
print("=== Caesar Cipher ===")
message = input("Enter your message: ")
shift = int(input("Enter shift value: "))

encrypted = caesar_cipher(message, shift, mode='encrypt')
print(f"Encrypted: {encrypted}")

decrypted = caesar_cipher(encrypted, shift, mode='decrypt')
print(f"Decrypted: {decrypted}")
