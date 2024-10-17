import hashlib
from PIL import Image
import random

def generate_salt(key):
    hashed_key = hashlib.sha256(str(key).encode()).hexdigest()
    return int(hashed_key, 16)  
def encrypt_image(image_path, key):
    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size

    salt = generate_salt(key)
    random.seed(salt)

    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]  
            
            operation = random.choice(['XOR', 'ADD', 'SUBTRACT'])
            
            if operation == 'XOR':
                r, g, b = r ^ key, g ^ key, b ^ key
            elif operation == 'ADD':
                r, g, b = (r + key) % 256, (g + key) % 256, (b + key) % 256
            elif operation == 'SUBTRACT':
                r, g, b = (r - key) % 256, (g - key) % 256, (b - key) % 256
            
            pixels[x, y] = (r, g, b)
    
    encrypted_image_path = image_path.split('.')[0] + "_encrypted_advanced.png"
    img.save(encrypted_image_path)
    print(f"Encrypted image saved as {encrypted_image_path}")

def decrypt_image(image_path, key):
    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size

    salt = generate_salt(key)
    random.seed(salt)

    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]  

            operation = random.choice(['XOR', 'ADD', 'SUBTRACT'])
            
            if operation == 'XOR':
                r, g, b = r ^ key, g ^ key, b ^ key
            elif operation == 'ADD':
                r, g, b = (r - key) % 256, (g - key) % 256, (b - key) % 256
            elif operation == 'SUBTRACT':
                r, g, b = (r + key) % 256, (g + key) % 256, (b + key) % 256

            pixels[x, y] = (r, g, b)

    decrypted_image_path = image_path.split('_encrypted')[0] + "_decrypted_advanced.png"
    img.save(decrypted_image_path)
    print(f"Decrypted image saved as {decrypted_image_path}")

def shuffle_blocks(image, block_size, key):
    width, height = image.size
    pixels = image.load()

    random.seed(key)
    
    blocks = []
    for x in range(0, width, block_size):
        for y in range(0, height, block_size):
            blocks.append((x, y))
    
    random.shuffle(blocks)
    
    new_image = Image.new('RGB', (width, height))
    new_pixels = new_image.load()

    for i, (x, y) in enumerate(blocks):
        block_x, block_y = blocks[i]
        for dx in range(block_size):
            for dy in range(block_size):
                if x + dx < width and y + dy < height:
                    new_pixels[x + dx, y + dy] = pixels[block_x + dx, block_y + dy]

    return new_image

def main():
    while True:
        print("\nAdvanced Image Encryption Tool")
        print("1. Encrypt an image")
        print("2. Decrypt an image")
        print("3. Exit")
        choice = input("Choose an option (1/2/3): ")

        if choice == '1':
            image_path = input("Enter the path of the image to encrypt: ")
            key = int(input("Enter a numerical key for encryption (e.g., 123): "))
            block_size = int(input("Enter block size for shuffling pixels (e.g., 8): "))

            img = Image.open(image_path)
            shuffled_img = shuffle_blocks(img, block_size, key)
            shuffled_img.save(image_path.split('.')[0] + "_shuffled.png")

            encrypt_image(image_path, key)

        elif choice == '2':
            image_path = input("Enter the path of the encrypted image to decrypt: ")
            key = int(input("Enter the key used for encryption: "))

            decrypt_image(image_path, key)

        elif choice == '3':
            print("Exiting the tool.")
            break
        
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
