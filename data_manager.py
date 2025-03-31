import pandas as pd
import json
import os
import random

def load_word_list(language):
    csv_path = f"assets/{language}_words.csv"
    json_path = f"progress/words_to_learn_{language}.json"

    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                words = json.load(f)
        except Exception:
            words = []
    else:
        df = pd.read_csv(csv_path)
        words = df.to_dict(orient="records")
        save_progress(language, words)

    return words

def save_progress(language, words_to_learn):
    json_path = f"progress/words_to_learn_{language}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(words_to_learn, f, ensure_ascii=False, indent=2)

def pick_random_word(word_list):
    return random.choice(word_list)

def load_csv_word_list(language):
    csv_path = f"assets/{language}_words.csv"
    df = pd.read_csv(csv_path)
    return df.to_dict(orient="records")
