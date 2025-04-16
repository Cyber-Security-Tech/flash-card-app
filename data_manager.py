import pandas as pd
import json
import os
import random

def load_word_list(language):
    """
    Loads the user's word list for the selected language.
    If progress exists in a JSON file, it loads that.
    Otherwise, it loads the full list from CSV and saves it to progress.

    Args:
        language (str): Language name (e.g. "French")

    Returns:
        list[dict]: List of word pairs as dictionaries
    """
    csv_path = f"assets/{language}_words.csv"
    json_path = f"progress/words_to_learn_{language}.json"

    words = []
    try:
        if os.path.exists(json_path):
            print(f"📦 Loading progress from: {json_path}")
            with open(json_path, "r", encoding="utf-8") as f:
                words = json.load(f)
        else:
            print(f"📄 No progress file found. Loading from: {csv_path}")
            df = pd.read_csv(csv_path)
            words = df.to_dict(orient="records")
            save_progress(language, words)
    except Exception as e:
        print(f"❌ Error loading word list: {e}")
        words = []

    # Filter out any rows with missing or blank values
    words = [
        w for w in words
        if w.get("English") and w.get(language.capitalize()) and w["English"].strip() and w[language.capitalize()].strip()
    ]

    print(f"✅ Loaded {len(words)} words for {language}")
    return words

def save_progress(language, words_to_learn):
    """
    Saves the current list of words to learn into a JSON progress file.

    Args:
        language (str): Language name
        words_to_learn (list[dict]): Remaining words the user hasn’t mastered
    """
    json_path = f"progress/words_to_learn_{language}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(words_to_learn, f, ensure_ascii=False, indent=2)

def pick_random_word(word_list):
    """
    Picks a random word from the given list.

    Args:
        word_list (list[dict]): List of words

    Returns:
        dict: A single word pair (foreign + English)
    """
    return random.choice(word_list)

def load_csv_word_list(language):
    """
    Loads the full list of words from the original CSV file.

    Args:
        language (str): Language name

    Returns:
        list[dict]: All word pairs from the CSV
    """
    csv_path = f"assets/{language}_words.csv"
    df = pd.read_csv(csv_path)
    return df.to_dict(orient="records")
