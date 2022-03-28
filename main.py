from tkinter import *
import random
import pandas
from tkinter import messagebox

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn= {}

# ------------------------------------------- Exception and Reading CSV --------------------------------------------------------#

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/german_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

# Orient is used to arrange keywords in dictionaries



# ------------------------------------------- New Flashcards --------------------------------------------------------#

def next_card():
    global current_card,flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    selected_card = current_card["German"]

    canvas.itemconfig(card_title,text="German",fill="black")
    canvas.itemconfig(card_word,text=selected_card,fill="black")
    canvas.itemconfig(canvas_image,image=card_front_photo)

    flip_timer = window.after(3000, func=flip_card)

def flip_card():

    selected_card = current_card["English"]

    canvas.itemconfig(card_title,text="English",fill="white")
    canvas.itemconfig(card_word,text=selected_card,fill="white")
    canvas.itemconfig(canvas_image,image=card_back_photo)


# ------------------------------------------- Saving CSV --------------------------------------------------------#

def is_known():
    to_learn.remove(current_card)

    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv",index=False)

    next_card()


# ------------------------------------------- Closing Window --------------------------------------------------------#

def save_file():
    if messagebox.askokcancel(title="Goodbye",message="Update Dictionary with recent improvement?"):
        data = pandas.DataFrame(to_learn)
        data.to_csv("data/words_to_learn.csv",index=False,mode="w")
        window.destroy()
    else:
        window.destroy()

# ------------------------------------------- UI Interface --------------------------------------------------------#

window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

window.protocol("WM_DELETE_WINDOW",save_file)

flip_timer = window.after(3000,func=flip_card)

canvas = Canvas(width=800, height=526)
card_back_photo = PhotoImage(file="images/card_back.png")
card_front_photo = PhotoImage(file="images/card_front.png")
canvas_image = canvas.create_image(400, 263, image=card_back_photo)

card_title = canvas.create_text(400, 150, text="German", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="word", font=("Ariel", 50, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)


# Buttons

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=next_card)
right_button.grid(row=1, column=0)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0,command=is_known)
wrong_button.grid(row=1, column=1)

next_card()

window.mainloop()
