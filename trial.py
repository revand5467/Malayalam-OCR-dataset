from PIL import Image
import random as random
import os

# Add a white background to the image
def add_white_background(img):
    background = Image.new('RGB', img.size, (255, 255, 255))
    background.paste(img, (0, 0), img)  # Use the image's transparency as the mask
    return background

def word_to_image(word, letter_image_mapping, gap=0):  # gap can be negative for overlap
    images_for_word = []
    
    for char in word:
        folder_name = f"character_{ord(char)}"
        if folder_name not in letter_image_mapping:
            print(f"Warning: No images found for character {char}. Skipping this character.")
            continue
        chosen_image_path = random.choice(letter_image_mapping[folder_name])
        with Image.open(chosen_image_path) as img:
            img_with_background = add_white_background(img)
            images_for_word.append(img_with_background)

    total_width = sum(img.width for img in images_for_word) + gap * (len(images_for_word) - 1)
    max_height = max(img.height for img in images_for_word)
    
    # Initialize the combined_img with a white background
    combined_img = Image.new('RGB', (total_width, max_height), (255, 255, 255))
    
    x_offset = 0
    for img in images_for_word:
        combined_img.paste(img, (x_offset, 0))
        x_offset += img.width + gap

    return combined_img

# Read the alphabet folders and get image paths
root_path = 'D:\AI\malayalam daataset'
alphabet_image_mapping = {}

for alphabet_folder in os.listdir(root_path):
    alphabet_path = os.path.join(root_path, alphabet_folder)
    if os.path.isdir(alphabet_path):
        alphabet_image_mapping[alphabet_folder] = [os.path.join(alphabet_path, image) for image in os.listdir(alphabet_path) if image.endswith(('.jpg', '.png'))]

# Read words from the dict.txt file
with open('dict.txt', 'r', encoding='utf-8') as f:
    words = [line.strip() for line in f]
    print(words)

# For each word, generate an image and save
output_directory = './output1'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

for word in words:
    word_image = word_to_image(word, alphabet_image_mapping, gap=-10)  # Adjust this value for the desired gap/overlap
    word_image.save(os.path.join(output_directory, f"{word}.png"))
