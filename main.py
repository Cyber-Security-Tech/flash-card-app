# main.py

from tkinter import *
import os
import json
import pandas as pd
from flashcard_ui import FlashCardApp
import data_manager

# ----- SUPPORTED LANGUAGES -----
SUPPORTED_LANGUAGES = ["french", "spanish", "german", "italian"]

class LanguageSelector:
    def __init__(self):
        self.window = Tk()
        self.window.title("Choose Language")
        self.window.config(padx=50, pady=50, bg="#B1DDC6")

        Label(self.window, text="Choose a language to learn:", font=("Ariel", 24, "bold"), bg="#B1DDC6").pack(pady=20)

        for lang in SUPPORTED_LANGUAGES:
            Button(
                text=lang.capitalize(),
                font=("Ariel", 18),
                width=20,
                command=lambda l=lang: self.handle_language(l)
            ).pack(pady=10)

        self.window.mainloop()

    def handle_language(self, language):
        self.window.destroy()
        self.show_progress_prompt(language)

    def show_progress_prompt(self, language):
        progress_path = f"progress/words_to_learn_{language}.json"
        original_csv_path = f"assets/{language}_words.csv"

        if os.path.exists(progress_path):
            try:
                with open(progress_path, "r", encoding="utf-8") as f:
                    saved_words = json.load(f)
                total_words = len(pd.read_csv(original_csv_path))
                remaining_words = len(saved_words)
            except Exception:
                saved_words = None

            # Show continue/reset prompt
            progress_window = Tk()
            progress_window.title("Continue or Reset")
            progress_window.config(padx=40, pady=40, bg="#B1DDC6")

            Label(progress_window,
                  text=f"You have {remaining_words} / {total_words} words left in {language.capitalize()}",
                  font=("Ariel", 16), bg="#B1DDC6").pack(pady=20)

            Button(progress_window, text="Continue", font=("Ariel", 14), width=20,
                   command=lambda: self.launch_app(progress_window, language)).pack(pady=10)

            Button(progress_window, text="Reset Progress", font=("Ariel", 14), width=20,
                   command=lambda: self.reset_and_launch(progress_window, language)).pack(pady=10)

            progress_window.mainloop()
        else:
            self.launch_app(None, language)

    def launch_app(self, win, language):
        if win:
            win.destroy()
        FlashCardApp(language=language)

    def reset_and_launch(self, win, language):
        if win:
            win.destroy()
        # Remove saved progress file
        progress_path = f"progress/words_to_learn_{language}.json"
        if os.path.exists(progress_path):
            os.remove(progress_path)
        FlashCardApp(language=language)

# Launch the language selection
LanguageSelector()
