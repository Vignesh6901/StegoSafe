import cv2
import numpy as np

# Function to hide a message using LSB technique
def hide_message(image_path, message):
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Image not found!")
        return
    
    # Convert message to binary and add an **end marker** to detect the message end
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    binary_message += '1111111111111110'  # End marker (16-bit sequence)

    data_index = 0
    total_pixels = img.shape[0] * img.shape[1] * 3  # Total color channels

    if len(binary_message) > total_pixels:
        print("Error: Message too long for this image.")
        return

    img_flat = img.flatten()
    
    for i in range(len(img_flat)):
        if data_index < len(binary_message):
            img_flat[i] = (img_flat[i] & 254) | int(binary_message[data_index])  # Modify LSB
            data_index += 1
        else:
            break

    img_encoded = img_flat.reshape(img.shape)
    cv2.imwrite("stego_image.png", img_encoded)  # Save as PNG (lossless)
    print("Message hidden successfully!")

# Function to extract the message
def extract_message(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Image not found!")
        return

    img_flat = img.flatten()
    binary_message = ""

    for i in range(len(img_flat)):
        binary_message += str(img_flat[i] & 1)

    # Convert binary to text until the **end marker** is found
    extracted_chars = []
    for i in range(0, len(binary_message), 8):
        char = chr(int(binary_message[i:i+8], 2))
        if binary_message[i:i+16] == '1111111111111110':  # Detect end marker
            break
        extracted_chars.append(char)

    extracted_message = "".join(extracted_chars)
    print("Decrypted message:", extracted_message.strip())

# Main execution
image_path = "bullet.jpg"
mode = input("Do you want to (1) Hide a message or (2) Extract a message? ")

if mode == "1":
    secret_message = input("Enter secret message: ")
    hide_message(image_path, secret_message)

elif mode == "2":
    extract_message("stego_image.png")

else:
    print("Invalid option!")
