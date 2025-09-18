import os

def caesar_cipher(text, shift, mode="encrypt"):
    result = ""
    if mode == "decrypt":
        shift = -shift

    for char in text:
        if char.isalpha():
            base = 65 if char.isupper() else 97
            result += chr((ord(char) - base + shift) % 26 + base)
        elif char.isdigit():
            result += chr((ord(char) - 48 + shift) % 10 + 48)
        else:
            result += char  # keep symbols/spaces unchanged
    return result


def brute_force_decrypt(text):
    print("\n=== Brute Force Results ===")
    for key in range(1, 26):
        attempt = caesar_cipher(text, key, "decrypt")
        print(f"Shift {key:2d}: {attempt}")


def save_to_file(filename, content):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"\n✅ Result saved to {filename}")


def main():
    while True:
        print("\n=== Caesar Cipher Tool ===")
        print("1. Encrypt a message")
        print("2. Decrypt a message")
        print("3. Brute-force decrypt")
        print("4. Exit")
        choice = input("Choose an option (1-4): ")

        if choice == "1":
            text = input("\nEnter your message: ")
            shift = int(input("Enter shift value: "))
            encrypted = caesar_cipher(text, shift, "encrypt")
            print("\n🔒 Encrypted:", encrypted)

            if input("Save to file? (y/n): ").lower() == "y":
                save_to_file("encrypted.txt", encrypted)

        elif choice == "2":
            text = input("\nEnter your encrypted message: ")
            shift = int(input("Enter shift value: "))
            decrypted = caesar_cipher(text, shift, "decrypt")
            print("\n🔓 Decrypted:", decrypted)

            if input("Save to file? (y/n): ").lower() == "y":
                save_to_file("decrypted.txt", decrypted)

        elif choice == "3":
            text = input("\nEnter your encrypted message: ")
            brute_force_decrypt(text)

        elif choice == "4":
            print("\n👋 Exiting program. Goodbye!")
            break
        else:
            print("❌ Invalid choice! Try again.")


if __name__ == "__main__":
    main()
