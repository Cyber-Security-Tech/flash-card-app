from tkinter import *
import data_manager
import os
import sys
import subprocess

BACKGROUND_COLOR = "#B1DDC6"

class FlashCardApp:
    def __init__(self, language):
        self.language = language
        self.word_list = data_manager.load_word_list(language)
        self.total_word_list = data_manager.load_csv_word_list(language)
        self.total_words = len(self.total_word_list)
        self.current_card = {}
        self.flip_timer = None

        self.window = Tk()
        self.window.title(f"{language.capitalize()} Flash Cards")
        self.window.config(padx=50, pady=30, bg=BACKGROUND_COLOR)

        # Load and store image references
        self.card_front_img = PhotoImage(file="images/card_front.png")
        self.card_back_img = PhotoImage(file="images/card_back.png")
        self.right_img = PhotoImage(file="images/right.png")
        self.wrong_img = PhotoImage(file="images/wrong.png")

        # Top Buttons: Home & Reset
        top_frame = Frame(self.window, bg=BACKGROUND_COLOR)
        top_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        Button(top_frame, text="🏠 Home", font=("Ariel", 12), command=self.go_home).pack(side=LEFT, padx=10)
        Button(top_frame, text="🔁 Reset", font=("Ariel", 12), command=self.reset_progress).pack(side=RIGHT, padx=10)

        # Canvas setup
        self.canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
        self.card_background = self.canvas.create_image(400, 263, image=self.card_front_img)
        self.card_title = self.canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
        self.card_word = self.canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
        self.canvas.grid(row=1, column=0, columnspan=2)

        # Progress Label
        self.progress_label = Label(
            text=f"Words remaining: {len(self.word_list)} / {self.total_words}",
            font=("Ariel", 14),
            bg=BACKGROUND_COLOR
        )
        self.progress_label.grid(row=2, column=0, columnspan=2, pady=10)

        # Buttons
        self.wrong_button = Button(image=self.wrong_img, highlightthickness=0, command=self.skip_word)
        self.wrong_button.grid(row=3, column=0)

        self.right_button = Button(image=self.right_img, highlightthickness=0, command=self.mark_known)
        self.right_button.grid(row=3, column=1)

        self.next_card()
        self.window.mainloop()

    def next_card(self):
        if self.flip_timer:
            self.window.after_cancel(self.flip_timer)

        if not self.word_list:
            self.canvas.itemconfig(self.card_title, text="Done!", fill="black")
            self.canvas.itemconfig(self.card_word, text="All words learned 🎉", fill="black", font=("Ariel", 40, "bold"))
            self.canvas.itemconfig(self.card_background, image=self.card_front_img)
            return

        self.current_card = data_manager.pick_random_word(self.word_list)
        self.canvas.itemconfig(self.card_title, text=self.language.capitalize(), fill="black")
        self.canvas.itemconfig(self.card_word, text=self.current_card[self.language.capitalize()], fill="black")
        self.canvas.itemconfig(self.card_background, image=self.card_front_img)
        self.flip_timer = self.window.after(3000, self.flip_card)

    def flip_card(self):
        self.canvas.itemconfig(self.card_title, text="English", fill="white")
        self.canvas.itemconfig(self.card_word, text=self.current_card["English"], fill="white")
        self.canvas.itemconfig(self.card_background, image=self.card_back_img)

    def mark_known(self):
        if self.current_card in self.word_list:
            self.word_list.remove(self.current_card)
            data_manager.save_progress(self.language, self.word_list)
            self.progress_label.config(text=f"Words remaining: {len(self.word_list)} / {self.total_words}")
        self.next_card()

    def skip_word(self):
        self.next_card()

    def reset_progress(self):
        progress_path = f"progress/words_to_learn_{self.language}.json"
        if os.path.exists(progress_path):
            os.remove(progress_path)
        self.window.destroy()
        FlashCardApp(language=self.language)

    def go_home(self):
        self.window.destroy()
        # Restart main.py (returns to language selector)
        subprocess.Popen([sys.executable, "main.py"])
        sys.exit()
