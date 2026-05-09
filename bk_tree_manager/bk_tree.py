import pickle


def levenshtein(a, b):
    if len(a) < len(b):
        return levenshtein(b, a)

    if len(b) == 0:
        return len(a)

    previous = range(len(b) + 1)

    for i, ca in enumerate(a):
        current = [i + 1]
        for j, cb in enumerate(b):
            insert = previous[j + 1] + 1
            delete = current[j] + 1
            replace = previous[j] + (ca != cb)
            current.append(min(insert, delete, replace))
        previous = current

    return previous[-1]


class BKNode:
    def __init__(self, word):
        self.word = word
        self.children = {}  # distance -> BKNode


class BKTree:
    def __init__(self):
        self.root = None

    def add(self, word: str):
        if self.root is None:
            self.root = BKNode(word)
            return

        node = self.root

        while True:
            dist = levenshtein(word, node.word)
            if dist == 0:
                break
            else:
                if dist in node.children:
                    node = node.children[dist]
                else:
                    node.children[dist] = BKNode(word)
                    break

    def search(self, word, max_distance=2) -> list[str]:
        if self.root is None:
            return []
        results = []

        def _search(node):
            dist = levenshtein(word, node.word)

            if dist <= max_distance:
                results.append(node.word)

            lower = dist - max_distance
            upper = dist + max_distance

            for child_dist, child_node in node.children.items():
                if lower <= child_dist <= upper:
                    _search(child_node)
        _search(self.root)
        return results

    def build(self, words: list[bytes]):
        for w in words:
            self.add(w.decode())

    def save(self, filename):
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load(filename):
        with open(filename, "rb") as f:
            return pickle.load(f)


