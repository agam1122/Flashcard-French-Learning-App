from tkinter import *
import pandas
import random

# Constant
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

# Try to load words to learn from a CSV file
try:
    data = pandas.read_csv('words_to_learn.csv')

# If the file is not found, load the original list of French words
except FileNotFoundError:
    original_data = data = pandas.read_csv('french_words.csv')
    to_learn = original_data.to_dict(orient='records')

# If the file is found, use it to populate the to_learn dictionary
else:
    to_learn = data.to_dict(orient='records')


def next_card():
    """
        Selects the next card to be displayed and starts a timer to flip it after 3 seconds.
    """
    global current_card, flip_timer
    # Cancel the previous flip timer
    window.after_cancel(flip_timer)
    # Choose a random card from the words to learn
    current_card = random.choice(to_learn)
    # Update the canvas with the French word and show the front of the card
    canvas.itemconfig(card_title, text="French", fill='Black')
    canvas.itemconfig(card_word, text=current_card['French'], fill='Black')
    canvas.itemconfig(card_background, image=card_front_img)
    # Start a timer to flip the card after 3 seconds
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    """
    Flips the current card to show the English translation.
    """
    canvas.itemconfig(card_title, text='English', fill='white')
    canvas.itemconfig(card_word, text=current_card['English'], fill='white')
    canvas.itemconfig(card_background, image=card_back_img)


def is_known():
    """
    Removes the current card from the words to learn and updates the CSV file.
    """
    to_learn.remove(current_card)
    next_card()
    data = pandas.DataFrame(to_learn)
    data.to_csv('words_to_learn.csv', index=False)



# Set up the main application window
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Set up the initial flip timer
flip_timer = window.after(3000, func=flip_card)

# Create a canvas to display the flashcards
canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file='card_front.png')
card_back_img = PhotoImage(file='card_back.png')
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, 'italic'))
card_word = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, 'bold'))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# Create buttons for marking words as known or unknown
cross_image = PhotoImage(file='wrong.png')
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file="right.png")
known_button = Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

# Display the first card
next_card()

# Start the main event loop
window.mainloop()
