import redis
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import nltk
import re
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()

retries = Retry(
    total=3,
    backoff_factor=1,       # wait: 1s, 2s, 4s...
    status_forcelist=[500, 502, 504],
    allowed_methods=["GET"]
)

adapter = HTTPAdapter(max_retries=retries)
session.mount("http://", adapter)
session.mount("https://", adapter)

nltk.download('stopwords')
nltk.download('punkt_tab')
r = redis.Redis(host='redis', port=6379, db=0)


def scrape_page(url_: dict[str, str]) -> list[str]:
    url = url_["url"]
    url_id = url_["id"]
    try:
        response = session.get(url, timeout=10)
        content_type = response.headers.get("Content-Type", "")
        if "text/html" not in content_type or response.status_code == 503:
            print(f"{url} URL does not return HTML content OR 503 CODE")
            return []
        print(f"Link = {url} id = {url_id}\n\n")
        soup = BeautifulSoup(response.text, "html.parser")

        # ---------------------------
        # 1. Extract and normalize links
        # ---------------------------
        raw_links = []
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            # ignore empty or javascript links
            if href.startswith("javascript:") or href.strip() == "":
                continue
            # normalize URL
            full_url = urljoin(url, href)
            raw_links.append(full_url)
        # remove duplicates
        urls_list = list(set(raw_links))

        # ---------------------------
        # 2. Extract text and clean HTML
        # ---------------------------
        text = soup.get_text(separator=" ")

        # remove non-alphabet characters
        text = re.sub(r"[^a-zA-Z\s]", " ", text)
        text = re.sub(r"\s+", " ", text).lower()

        # ---------------------------
        # 3. Stopwords + Snowball stemming
        # ---------------------------
        stop_words = set(stopwords.words("english"))
        stemmer = SnowballStemmer("english")

        for word in nltk.word_tokenize(text):
            if word not in stop_words and len(word) > 2:
                stemmed = stemmer.stem(word)
                r.rpush(f"crawler_{stemmed}", url_id)
    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return []

    return urls_list


