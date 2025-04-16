# Suppress Tkinter callback exceptions (optional: prevents noisy terminal errors)
import tkinter
tkinter.Tk.report_callback_exception = lambda *args: None

import tkinter as tk
from tkinter import TclError, messagebox
from PIL import Image, ImageTk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import data_manager
import os

class FlashCardApp:
    """
    Flash card application for language learning.
    Allows user to flip cards, mark known words, and track progress.
    """

    def __init__(self, language):
        """
        Initialize the flashcard app window and UI.
        Args:
            language (str): Selected language (e.g. "French")
        """
        self.language = language
        self.window = ttk.Window(themename="flatly")
        self.window.title(f"{language.capitalize()} Flash Cards")
        self.window.geometry("900x700")
        self.window.resizable(False, False)

        # Internal state flags
        self.is_exiting = False
        self.flip_step = 0
        self.is_flipping = False
        self.flip_timer = None

        # Ensure clean exit on window close
        self.window.protocol("WM_DELETE_WINDOW", self.exit_cleanly)

        self.load_images()
        self.build_ui()
        self.window.mainloop()

    def load_images(self):
        """
        Load and resize all card and button images used in the UI.
        """
        self.card_front_img_raw = Image.open("images/card_front.png").resize((800, 500))
        self.card_back_img_raw = self.card_front_img_raw  # Reuse same image visually
        self.right_img = ImageTk.PhotoImage(Image.open("images/right.png").resize((64, 64)))
        self.wrong_img = ImageTk.PhotoImage(Image.open("images/wrong.png").resize((64, 64)))

    def build_ui(self):
        """
        Construct the main flashcard interface: canvas, buttons, and labels.
        """
        # Load word list and total words for progress tracking
        self.word_list = [
            word for word in data_manager.load_word_list(self.language)
            if word.get("English") and word.get(self.language.capitalize())
        ]
        self.total_word_list = data_manager.load_csv_word_list(self.language)
        self.total_words = len(self.total_word_list)
        self.current_card = {}

        # Clear any existing widgets
        for widget in self.window.winfo_children():
            widget.destroy()

        # Top navigation buttons
        top_frame = ttk.Frame(self.window)
        top_frame.pack(fill=tk.X, pady=5, padx=10)
        ttk.Button(top_frame, text="🏠 Home", bootstyle="secondary-outline", command=self.go_home).pack(side=tk.LEFT)
        ttk.Button(top_frame, text="🔁 Reset", bootstyle="secondary-outline", command=self.reset_progress).pack(side=tk.RIGHT)

        # Flashcard canvas (main display area)
        self.canvas = tk.Canvas(self.window, width=800, height=500, highlightthickness=0, bg="#B1DDC6")
        self.canvas.pack(pady=(10, 10))

        # Progress label
        self.progress_label = ttk.Label(
            text=f"Words remaining: {len(self.word_list)} / {self.total_words}",
            font=("Segoe UI", 12),
            bootstyle="info"
        )
        self.progress_label.pack(pady=(0, 10))

        # Right/Wrong buttons
        button_frame = ttk.Frame(self.window)
        button_frame.pack(pady=(0, 20))
        self.wrong_button = ttk.Button(button_frame, image=self.wrong_img, command=self.flip_back_then_next, bootstyle="outline-danger")
        self.right_button = ttk.Button(button_frame, image=self.right_img, command=self.mark_known, bootstyle="success")
        self.wrong_button.grid(row=0, column=0, padx=30)
        self.right_button.grid(row=0, column=1, padx=30)

        self.next_card()

    def next_card(self):
        """
        Show the next flashcard and start flip animation timer.
        """
        if self.is_exiting:
            return
        if self.flip_timer:
            try:
                self.window.after_cancel(self.flip_timer)
            except:
                pass
            self.flip_timer = None

        # If word list is empty, show final card
        if not self.word_list:
            self.show_card(front=True, final=True)
            return

        # Pick and display a new word
        self.current_card = data_manager.pick_random_word(self.word_list)
        self.show_card(front=True)
        try:
            self.flip_timer = self.window.after(3000, self.animate_flip)
        except:
            pass

    def show_card(self, front=True, final=False, width=800):
        """
        Display either the front (foreign) or back (English) side of a flashcard.
        Args:
            front (bool): True = show front of card, False = back
            final (bool): True if this is the last card message
            width (int): Width for flip animation
        """
        if self.is_exiting:
            return

        self.canvas.delete("all")
        img_raw = self.card_front_img_raw if front else self.card_back_img_raw
        resized_img = img_raw.resize((width, 500))
        self.current_image = ImageTk.PhotoImage(resized_img)
        self.canvas.create_image(400, 250, image=self.current_image)

        # Card content
        if final:
            title = "Done!"
            word = "All words learned 🎉"
            color = "black"
        elif front:
            title = self.language.capitalize()
            word = self.current_card[self.language.capitalize()]
            color = "black"
        else:
            title = "English"
            word = self.current_card["English"]
            color = "white"

        self.canvas.create_text(400, 160, text=title, font=("Segoe UI", 28, "italic"), fill=color)
        self.canvas.create_text(400, 270, text=word, font=("Segoe UI", 36, "bold"), fill=color)

    def animate_flip(self):
        """
        Start the card flip animation (front → back).
        """
        if self.is_exiting or self.is_flipping:
            return
        self.is_flipping = True
        self.flip_step = 0
        self._animate_flip_step(reverse=False)

    def flip_back_then_next(self):
        """
        Flip the card from back → front, then move to next card.
        (Used when marking a word as unknown.)
        """
        if self.is_exiting or self.is_flipping:
            return
        self.is_flipping = True
        self.flip_step = 0
        self._animate_flip_step(reverse=True)

    def _animate_flip_step(self, reverse=False):
        """
        Perform one step of the card flip animation.
        Args:
            reverse (bool): True = back→front flip (wrong), False = front→back flip (auto)
        """
        if self.is_exiting:
            return
        total_steps = 10
        midpoint = total_steps // 2

        if self.flip_step <= total_steps:
            progress = self.flip_step / total_steps
            scale = 1 - abs(0.5 - progress) * 2
            width = max(1, int(800 * scale))

            if reverse:
                show_front = self.flip_step >= midpoint
                self.show_card(front=show_front, width=width)
            else:
                show_front = self.flip_step < midpoint
                self.show_card(front=show_front, width=width)

            self.flip_step += 1
            if not self.is_exiting and self.window.winfo_exists():
                self.window.after(30, lambda: self._animate_flip_step(reverse))
        else:
            self.is_flipping = False
            if reverse:
                self.window.after(300, self.next_card)
            else:
                self.show_card(front=False)

    def mark_known(self):
        """
        Mark the current word as known, remove from word list, and update progress.
        """
        if self.is_exiting or self.is_flipping:
            return
        if self.current_card in self.word_list:
            self.word_list.remove(self.current_card)
            data_manager.save_progress(self.language, self.word_list)
            self.progress_label.config(text=f"Words remaining: {len(self.word_list)} / {self.total_words}")
        self.next_card()

    def reset_progress(self):
        """
        Delete the progress file for the current language and reload all words.
        """
        if self.is_exiting:
            return
        progress_path = f"progress/words_to_learn_{self.language}.json"
        if os.path.exists(progress_path):
            os.remove(progress_path)
        self.build_ui()

    def go_home(self):
        """
        Return to the home screen and destroy current window.
        """
        if self.is_exiting:
            return
        from main import launch_home
        self.window.destroy()
        launch_home()

    def exit_cleanly(self):
        """
        Gracefully exit the app and cancel any pending animations.
        """
        self.is_exiting = True
        try:
            if self.flip_timer:
                self.window.after_cancel(self.flip_timer)
        except:
            pass
        self.window.destroy()