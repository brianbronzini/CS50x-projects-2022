# TODO

# User input
text = input("Text: ")
length = len(text)

# Initialize counter variables
letter = word = sentence = 0

# Loop through entire string
for char in text:

    # Count letters
    if char.isalpha():
        letter += 1
    # Count words
    if char.isspace():
        word += 1
    # Count sentences
    if char in ["?", ".", "!"]:
        sentence += 1

# Increment for more complex test cases
word += 1

# Declare new variables for Coleman-Liau index formula
L = (letter * 100) / word
S = (sentence * 100) / word
formula = round(0.0588 * L - 0.296 * S - 15.8)

# Print outputs
if formula < 1:
    print("Before Grade 1")
elif formula >= 16:
    print("Grade 16+")
else:
    print(f"Grade {formula}")
