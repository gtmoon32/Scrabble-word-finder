from tqdm import tqdm
import sys
from PIL import Image
import pytesseract
import enchant
import itertools

# Define the letter scores based on the provided scoring system
letter_scores = {
    'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1,
    'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1,
    'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10
}

def extract_letters(image_path):
    try:
        # Use Tesseract OCR to extract text from the image
        raw_ocr_output = pytesseract.image_to_string(image_path, config='--psm 10 eng')

        # Print the raw OCR output
        print("Raw OCR Output:")
        print(raw_ocr_output)

        # Process the extracted text to get individual letters
        letters = [char.upper() for char in raw_ocr_output if char.isalpha()]

        return letters

    except Exception as e:
        print(f"Error during OCR: {e}")
        sys.exit(1)  # Exit the script with an error code

def calculate_word_score(word):
    # Calculate the score for a given word
    base_score = sum(letter_scores[letter] for letter in word)
    
    return base_score

def load_valid_words(filename):
    with open(filename, 'r') as file:
        return set(word.strip().lower() for word in file)

def is_valid_word(word, valid_words_set):
    return word.lower() in valid_words_set

def find_highest_scoring_word(letters, valid_words_set):
    # Find all possible combinations of letters
    all_combinations = itertools.chain.from_iterable(itertools.permutations(letters, r) for r in range(3, 9))

    # Calculate the total number of combinations for the progress bar
    total_combinations = sum(1 for _ in all_combinations)

    # Reset the iterator after calculating total_combinations
    all_combinations = itertools.chain.from_iterable(itertools.permutations(letters, r) for r in range(3, 9))

    # Initialize the progress bar
    progress_bar = tqdm(total=total_combinations, desc="Checking words")

    # Find the highest-scoring and valid word
    highest_score = 0
    highest_word = ""

    for combination in tqdm(all_combinations, desc="Checking Combinations", total=total_combinations, leave=False):
        word = ''.join(combination)
        if is_valid_word(word, valid_words_set):
            score = calculate_word_score(word)
            if score > highest_score:
                highest_score = score
                highest_word = word

        # Update the progress bar
        progress_bar.update(1)

    # Close the progress bar
    progress_bar.close()

    return highest_word, highest_score

# Example usage
try:
    cube_image_path = 'word.png'
    valid_words_filename = 'words.txt'

    letters_on_cube = extract_letters(cube_image_path)
    valid_words_set = load_valid_words(valid_words_filename)
    highest_word, highest_score = find_highest_scoring_word(letters_on_cube, valid_words_set)

    print('Letters on the cube:', letters_on_cube)
    print('Highest-scoring word:', highest_word)
    print('Score:', highest_score)

except Exception as e:
    print(f"An unexpected error occurred: {e}")
