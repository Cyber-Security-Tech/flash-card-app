from flashcard_ui import FlashCardApp  # Import the main flashcard app class from the UI module
import ttkbootstrap as ttk  # Use ttkbootstrap for modern themed Tkinter components

def launch_home():
    """
    Displays the home screen where the user selects a language to learn.
    """
    # Create the root window with a modern flat theme
    window = ttk.Window(themename="flatly")
    window.title("Language Flash Cards")
    window.geometry("400x300")  # Fixed window size
    window.resizable(False, False)  # Disable resizing

    # Title label
    label = ttk.Label(window, text="Select a Language", font=("Segoe UI", 20))
    label.pack(pady=20)

    # List of supported languages
    languages = ["French", "German", "Italian", "Spanish"]

    # Create a button for each language
    for lang in languages:
        ttk.Button(
            window,
            text=lang,
            width=20,
            bootstyle="primary",  # Bootstrap-styled button
            command=lambda l=lang: launch_flashcards(l, window)  # Pass selected language
        ).pack(pady=5)

    # Start the main GUI loop
    window.mainloop()

def launch_flashcards(language, parent_window):
    """
    Closes the home screen and launches the flashcard UI for the selected language.
    
    Args:
        language (str): The selected language (e.g., "French").
        parent_window (ttk.Window): The home screen window to close.
    """
    parent_window.destroy()         # Close the home screen
    FlashCardApp(language)          # Launch the flashcard UI for the chosen language

# Start the app if this file is run directly
if __name__ == "__main__":
    launch_home()
