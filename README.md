# 🧠 FlashCard Pro – Multi-Language Desktop App

An elegant, animated flashcard app that helps you master daily conversational vocabulary in multiple languages.

---

## 🚀 Features

- 🔤 **Supports Multiple Languages** (French, German, Italian, Spanish)
- 🧠 **Learn Mode**: Automatically flips flashcards to show English translation
- ❌✅ **Track Progress**: Mark known words, and they won't reappear
- 💾 **Persistent Progress**: Saves your learned words even after closing the app
- 🔁 **Reset Anytime**: Reset your progress and start fresh
- 🏠 **Home Navigation**: Switch languages or restart from the main screen
- ✨ **Polished Flip Animation**: Smooth card flip (front to back) and return animation when pressing ❌
- 🪄 **Professional UI**: Built with `ttkbootstrap` for a modern, stylish look
- 🧯 **Safe Exit Handling**: Clean shutdown with no terminal errors

---

## 📂 Folder Structure

```
flash_card_app/
│
├── data/                  # Contains CSV word lists (e.g., french_words.csv)
├── progress/              # Stores user progress in JSON
├── images/                # All card images and icons
├── main.py                # Launches the home screen
├── flashcard_ui.py        # Core GUI and logic
└── README.md              # This file
```

---

## 🧪 Technologies Used

- `Python 3`
- `Tkinter`
- `PIL` (Pillow)
- `ttkbootstrap`
- `pandas` (for CSV reading)

---

## 🛠️ Installation

1. Clone the repo:
```bash
git clone https://github.com/your-username/flashcard-pro.git
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
python main.py
```

---

## 💡 Future Ideas

- Web version using Flask or Django
- Sound effects
- Dark/light mode toggle
- Keyboard support

---

## 📜 License

MIT — free to use, modify, and learn from.