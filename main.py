from tkinter import *
from random import choice

# Globals
FONT_INPUT = ('Arial', 30, 'normal')
FONT_STATS = ('Arial', 18, 'normal')
FONT_WRONG = ('Arial', 14, 'normal')
TEST_LENGTH = 10  # In Seconds
chosen_words = []
submitted_words = []
WINDOW_WIDTH = 500
WINDOW_HEIGHT_MAX = 300
WINDOW_HEIGHT_MIN = 300

# Grab Words
with open('words.txt', 'r') as file:
    # TODO: Just have a body of text or webscrape from https://english4today.com/500-most-used-words-in-english/
    words = file.read().lower().replace('\n', ' ').split(" ")

    # Removes repeated words from txt file
    # Changed words.txt from a paragraph to a list of words, uncomment if changing words.txt
    # into a paragraph of random text, and changed the above words to raw_words
    # words = []
    # for word in raw_words:
    #     if word not in words:
    #         words.append(word)


# Meat
def next_word(event):
    # TODO: Have a preview of next word, by grabbing ~100 words on start_test rather than in next_word
    global chosen_words, submitted_words
    if word_input.get() == "":
        submitted_words.append("SK!P")
    else:
        submitted_words.append(word_input.get().lower())
    word_input.delete(0, END)

    # TODO: Cycle to next item in chosen_word list rather than add to the list
    new_word = choice(words)
    chosen_words.append(new_word)
    word_title['text'] = new_word


def end_test():
    word_input['text'] = ""
    word_input.config(state=DISABLED)
    # Expands window size to encompass all incorrect words, if there are any 😉
    window.maxsize(WINDOW_WIDTH, WINDOW_HEIGHT_MAX + (len(chosen_words) * 25))

    # Removing first index as when we call first call next_word() the first index is empty
    submitted_words.pop(0)

    # WPM formula  ( Characters / 5 ) / minutes

    inaccurate_words = ""
    characters = 0
    for i in range(len(submitted_words)):
        if submitted_words[i] == "SK!P":
            inaccurate_words += f"You skipped {chosen_words[i]}\n"
        elif submitted_words[i] != chosen_words[i]:
            inaccurate_words += f"Instead of '{chosen_words[i]}', you typed '{submitted_words[i]}'\n"
        else:
            characters += len(submitted_words[i])

    raw_words = [word for word in submitted_words if word != "SK!P"]
    wrong_words['text'] = inaccurate_words
    if inaccurate_words != "":
        raw_wpm_label['text'] = f"Raw WPM = {float((len(''.join(raw_words)) / 5) / (TEST_LENGTH / 60)):.1f}"
        prefix = "Accurate "
    else:
        prefix = ""

    wpm_label['text'] = f"{prefix}WPM = {float((characters / 5) / (TEST_LENGTH / 60)):.1f}"


def start_test(event):
    if word_input.get().lower() == 'start':
        word_input.delete(0, END)
        next_word(event)
        window.bind('<Return>', next_word)

        # Seconds * 1000 gives time in milliseconds
        window.after(TEST_LENGTH * 1000, end_test)


def reset_ui():
    word_title['text'] = "Type start and press enter"
    word_input.config(state=NORMAL)
    word_input.delete(0, END)
    raw_wpm_label['text'] = ""
    wpm_label['text'] = ""
    wrong_words['text'] = ""
    window.bind('<Return>', start_test)
    window.maxsize(WINDOW_WIDTH, WINDOW_HEIGHT_MIN)
    window.maxsize(WINDOW_WIDTH, WINDOW_HEIGHT_MAX)


# Interface Setup
# TODO: Make it look pretty, low priority
window = Tk()
window.title("Typing Speed Calculator")
window.maxsize(WINDOW_WIDTH, WINDOW_HEIGHT_MAX)
window.minsize(WINDOW_WIDTH, WINDOW_HEIGHT_MIN)

# Type Space
word_title = Label(text="Type start and press enter", font=FONT_INPUT)
word_title.pack(pady=(20, 20))
word_input = Entry(width=17, justify=CENTER, font=FONT_INPUT)
word_input.pack()

# Stat Space
raw_wpm_label = Label(text="", font=FONT_STATS)
raw_wpm_label.pack()
wpm_label = Label(text="", font=FONT_STATS)
wpm_label.pack()
wrong_words = Label(text="", font=FONT_WRONG, justify=LEFT)
wrong_words.pack()

reset_button = Button(text="Reset", command=reset_ui)
reset_button.pack()

# Keybind Setup
window.bind('<Return>', start_test)

window.mainloop()
