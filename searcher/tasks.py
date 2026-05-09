import os
from concurrent.futures import ThreadPoolExecutor
from bk_tree_manager.models import Word, WordURL
from bk_tree_manager.serializers import WordSerializer
from celery import shared_task
import re
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import nltk
from bk_tree_manager.bk_tree import BKTree
from itertools import repeat
import pickle


def arrange_words(text: str) -> set[str]:
    # remove non-alphabet characters
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).lower()
    # Stopwords + Snowball stemming
    stop_words = set(stopwords.words("english"))
    stemmer = SnowballStemmer("english")
    final_result: set[str] = set([])

    for word in nltk.word_tokenize(text):
        if word not in stop_words and len(word) > 2:
            stemmed = stemmer.stem(word)
            final_result.add(stemmed)
    return final_result


def get_result(word: str, tree: BKTree, level=1):
    word_obj = Word.objects.get(word=word)
    data = WordSerializer(word_obj).data
    if len(data.get("urls")) > 0 or level == 2:
        print(data)
        return data
    else:
        result = []
        new_words = tree.search(word, max_distance=3)
        for w in new_words:
            result += get_result(w, tree, level=2)
        return result


@shared_task
def search(search_sentence: str):
    key_words = arrange_words(search_sentence)
    print(key_words)
    tree = BKTree.load(f"{os.environ.get('WORD_DICT_NAME')}.pkl")
    with ThreadPoolExecutor(max_workers=int(os.environ.get("MAX_THREADS", 10))) as executor:
        results = executor.map(get_result, key_words, repeat(tree))

    print(results)



