from flashcard_ui import FlashCardApp
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def launch_home():
    # Home screen for language selection
    window = ttk.Window(themename="flatly")
    window.title("Language Flash Cards")
    window.geometry("400x300")
    window.resizable(False, False)

    label = ttk.Label(window, text="Select a Language", font=("Segoe UI", 20))
    label.pack(pady=20)

    languages = ["French", "German", "Italian", "Spanish"]
    for lang in languages:
        ttk.Button(
            window,
            text=lang,
            width=20,
            bootstyle="primary",
            command=lambda l=lang: launch_flashcards(l, window)
        ).pack(pady=5)

    window.mainloop()

def launch_flashcards(language, parent_window):
    parent_window.destroy()  # Close the home window
    FlashCardApp(language)   # Launch flashcard UI

if __name__ == "__main__":
    launch_home()
