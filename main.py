from tkinter import *
from flashcard_ui import FlashCardApp

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
        FlashCardApp(language=language)

# Launch selector
LanguageSelector()
