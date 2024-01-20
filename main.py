from tkinter import *
from random import choice
import pandas
BACKGROUND_COLOR = "#B1DDC6"
GUESSES_RIGHT = 0
GUESSES_WRONG = 0
FONT_NAME = 'calibri'
CURRENT_CARD = {}

# -----------------------------------------------GETTING RANDOM WORD-----------------------------------------------#
data = pandas.read_csv('data/french_words.csv')
data_dict = data.to_dict(orient='records')


def flip_card():
    global CURRENT_CARD
    canvas.itemconfig(canvas_image, image=card_back)
    canvas.itemconfig(word_text, fill='white', text=f'{CURRENT_CARD["English"]}')
    canvas.itemconfig(language_text, fill='white', text='English')


def get_word():
    global CURRENT_CARD, flip_timer
    window.after_cancel(flip_timer)
    canvas.itemconfig(canvas_image, image=card_front)
    CURRENT_CARD = choice(data_dict)
    canvas.itemconfig(word_text, fill='black', text=f"{CURRENT_CARD['French']}")
    canvas.itemconfig(language_text, fill='black', text='French')
    flip_timer = window.after(3000, flip_card)


def is_known():
    data_dict.remove(CURRENT_CARD)
    print(len(data_dict))
    data = pandas.DataFrame(data_dict)
    data.to_csv('data/words_to_learn.csv')
    get_word()


# -----------------------------------------------UI SETUP-----------------------------------------------#
window = Tk()
window.title("Flash Cards")
window.config(padx=60, pady=60, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, flip_card)

# -----------------------------------------------IMAGES-----------------------------------------------#
check_image = PhotoImage(file='images/right.png')
x_image = PhotoImage(file='images/wrong.png')
card_back = PhotoImage(file='images/card_back.png')
card_front = PhotoImage(file='images/card_front.png')

# -----------------------------------------------BUTTONS-----------------------------------------------#
correct_button = Button(image=check_image, highlightthickness=0, command=is_known)
correct_button.grid(row=1, column=1)
wrong_button = Button(image=x_image, highlightthickness=0, command=get_word)
wrong_button.grid(row=1, column=0)

# -----------------------------------------------FLASH CARDS-----------------------------------------------#
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas_image = canvas.create_image(400, 263, image=card_front)
language_text = canvas.create_text(400, 135, text='Title', font=(FONT_NAME, 40, 'italic'))
word_text = canvas.create_text(400, 263, text='Word', font=(FONT_NAME, 60, 'bold'))
canvas.grid(row=0, column=0, columnspan=2)

get_word()
window.mainloop()
