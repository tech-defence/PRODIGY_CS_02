from PIL import Image
import os
from tast2_art import logo,greet_by # Import the logo and created_by information

# ANSI escape codes for colors
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

class ImageEncryptor:
    def __init__(self, key):
        self.key = key

    def encrypt(self, image_path):
        try:
            img = Image.open(image_path)
        except IOError:
            print(f"Error: Cannot open image file {image_path}. Please check the file path and format.")
            return None
        
        width, height = img.size
        encrypted_img = Image.new(mode=img.mode, size=(width, height))
        
        for x in range(width):
            for y in range(height):
                pixel = img.getpixel((x, y))
                if isinstance(pixel, int):  # Grayscale image
                    encrypted_pixel = (pixel + self.key) & 255
                else:  # RGB or RGBA image
                    encrypted_pixel = tuple((p + self.key) & 255 for p in pixel)
                encrypted_img.putpixel((x, y), encrypted_pixel)
        
        directory, filename = os.path.split(image_path)
        name, extension = os.path.splitext(filename)
        encrypted_image_path = os.path.join(directory, f"encrypted_image{extension}")
        
        encrypted_img.save(encrypted_image_path)
        print(f"Image encrypted and saved to {encrypted_image_path}.")
        return encrypted_img, directory, extension

    def decrypt(self, encrypted_image, directory, extension):
        width, height = encrypted_image.size
        decrypted_img = Image.new(mode=encrypted_image.mode, size=(width, height))
        
        for x in range(width):
            for y in range(height):
                encrypted_pixel = encrypted_image.getpixel((x, y))
                if isinstance(encrypted_pixel, int):  # Grayscale image
                    decrypted_pixel = (encrypted_pixel - self.key) % 256
                else:  # RGB or RGBA image
                    decrypted_pixel = tuple((p - self.key) % 256 for p in encrypted_pixel)
                decrypted_img.putpixel((x, y), decrypted_pixel)
        
        decrypted_image_path = os.path.join(directory, f"decrypted_image{extension}")
        decrypted_img.save(decrypted_image_path)
        print(f"Image decrypted and saved to {decrypted_image_path}.")
        return decrypted_img

def main():
    key = 123
    
    # Display the logo in green and created_by in red
    print(GREEN + logo + RESET)
    
    while True:
        print("Choose an option:")
        print("1. Encrypt an image")
        print("2. Decrypt an image")
        print("0. Exit")
        
        choice = input("Enter your choice (0-2): ")
        
        if choice == "0":
            print("Exiting the program...")
            print(GREEN + greet_by + RESET)
            break
        elif choice == "1":
            image_path = input("Enter the path of the image to encrypt: ")
            
            encryptor = ImageEncryptor(key)
            encrypted_image, directory, extension = encryptor.encrypt(image_path)
            
            if encrypted_image:
                encrypted_image.show(title="Encrypted Image")
        elif choice == "2":
            image_path = input("Enter the path of the encrypted image: ")
            
            try:
                img = Image.open(image_path)
            except IOError:
                print(f"Error: Cannot open image file {image_path}. Please check the file path and format.")
                continue
            
            directory, filename = os.path.split(image_path)
            name, extension = os.path.splitext(filename)
            
            encryptor = ImageEncryptor(key)
            decrypted_image = encryptor.decrypt(img, directory, extension)
            decrypted_image.show(title="Decrypted Image")
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()