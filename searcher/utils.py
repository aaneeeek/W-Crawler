import re

import nltk
from nltk import SnowballStemmer
from nltk.corpus import stopwords

from bk_tree_manager.bk_tree import BKTree
from bk_tree_manager.models import Word
from bk_tree_manager.serializers import WordSerializer, URLSerializer


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


def get_result(word: str, tree: BKTree, level=1) -> list[dict[str, dict[str, str]]]:
    try:
        word_obj = Word.objects.get(word=word)
        data = URLSerializer(word_obj.word_url.all(), many=True).data
        if len(data) > 0 or level == 3:
            print("length was not 0 **************************")
            print(data)
            return data
        else:
            print("length was 0 ###########################")
            result = []
            new_words = tree.search(word, max_distance=3)
            for w in new_words:
                result += get_result(w, tree, level=3)
            return result
    except Exception as e:
        print(f"Word not found ----------------------- {e}")
        result = []
        new_words = tree.search(word, max_distance=3)
        for w in new_words:
            result += get_result(w, tree, level=3)
        return result

