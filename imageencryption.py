"""
Image Encryption Tool
---------------------
This program demonstrates simple image encryption and decryption
using pixel manipulation techniques. It supports:
1. Mathematical pixel operations (e.g., XOR with a key).
2. Swapping pixel values.

Author: Your Name
Date: YYYY-MM-DD
"""

from PIL import Image
import random


def encrypt_decrypt_math(image_path, key, output_path):
    """
    Encrypt or decrypt an image using XOR operation on pixel values.
    XOR with the same key twice returns the original image.
    """
    img = Image.open(image_path)
    pixels = img.load()

    for x in range(img.width):
        for y in range(img.height):
            r, g, b = pixels[x, y]
            # Apply XOR with key to each channel
            pixels[x, y] = (r ^ key, g ^ key, b ^ key)

    img.save(output_path)
    print(f"Image saved at: {output_path}")


def encrypt_swap(image_path, output_path):
    """
    Encrypt an image by swapping pixels in a random pattern.
    (Decryption requires applying the same swaps in reverse order).
    """
    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size

    # Generate random swap positions
    swaps = []
    for _ in range(5000):  # swap 5000 pairs of pixels
        x1, y1 = random.randint(0, width-1), random.randint(0, height-1)
        x2, y2 = random.randint(0, width-1), random.randint(0, height-1)
        pixels[x1, y1], pixels[x2, y2] = pixels[x2, y2], pixels[x1, y1]
        swaps.append(((x1, y1), (x2, y2)))

    img.save(output_path)
    print(f"Image saved at: {output_path}")
    return swaps  # save swap history for decryption


def decrypt_swap(image_path, output_path, swaps):
    """
    Decrypt an image by reversing the pixel swaps.
    """
    img = Image.open(image_path)
    pixels = img.load()

    for (x1, y1), (x2, y2) in reversed(swaps):
        pixels[x1, y1], pixels[x2, y2] = pixels[x2, y2], pixels[x1, y1]

    img.save(output_path)
    print(f"Decrypted image saved at: {output_path}")


# Example Usage
if __name__ == "__main__":
    # XOR-based encryption/decryption
    encrypt_decrypt_math("input.jpg", key=123, output_path="encrypted_math.jpg")
    encrypt_decrypt_math("encrypted_math.jpg", key=123, output_path="decrypted_math.jpg")

    # Pixel swapping encryption/decryption
    swap_history = encrypt_swap("input.jpg", "encrypted_swap.jpg")
    decrypt_swap("encrypted_swap.jpg", "decrypted_swap.jpg", swap_history)
