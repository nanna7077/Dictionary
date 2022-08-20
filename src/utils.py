import json
import os
from difflib import get_close_matches

dict_en = {}
currentHist = []


def load_history(language):
    global currentHist
    if os.name == "posix":
        histfile = os.path.expanduser(f"~/.dictionaryHist{language}")
    else:
        # Implemenet for others
        return
    try:
        with open(histfile, "r") as f:
            currentHist = [l.strip() for l in f.readlines()]
            currentHist = currentHist[::-1]
    except:
        return


def save_history(language, word):
    global currentHist
    if word in currentHist:
        currentHist.remove(word)
    if os.name == "posix":
        histfile = os.path.expanduser(f"~/.dictionaryHist{language}")
    else:
        # Implemenet for others
        return
    if len(currentHist) >= 25:
        currentHist = currentHist[0:24]
    currentHist = currentHist[::-1]
    currentHist.append(word.lower().title())
    with open(histfile, "w") as f:
        for i in currentHist:
            f.write(i)
            f.write("\n")
    currentHist = currentHist[::-1]


def clear_history(language):
    global currentHist
    if os.name == "posix":
        histfile = os.path.expanduser(f"~/.dictionaryHist{language}")
    else:
        # Implemenet for others
        return
    with open(histfile, "w") as f:
        f.truncate(0)
    currentHist = []


def en_search(word):
    word = word.upper()
    if word in dict_en:
        return word.lower().title(), dict_en[word], True
    closest_match = get_close_matches(word, dict_en.keys())[0]
    if closest_match != None:
        return closest_match.lower().title(), dict_en[closest_match], False


# Loading EN Dictionary, loading can be changed into based on user preference in the future when support for other language are added.

with open("en.json", "r") as en_txt:
    dict_en = json.loads(en_txt.read())

load_history("en")  # Change to be based on user preference.
