import json
from difflib import get_close_matches

dict_en={}

def en_search(word):
    word=word.upper()
    if word in dict_en:
        return word.lower().title(), dict_en[word], True
    closest_match=get_close_matches(word, dict_en.keys())[0]
    if closest_match!=None:
        return closest_match.lower().title(), dict_en[closest_match], False

#Loading EN Dictionary, loading can be changed into based on user preference in the future when support for other language are added.

with open('en.json', 'r') as en_txt:
    dict_en=json.loads(en_txt.read())