import os
from concurrent.futures import ThreadPoolExecutor
from celery import shared_task
from .models import URLs, Word, WordURL
from .scrapper import scrape_page
from .serializers import URLSerializer
from .bk_tree import BKTree

import redis

r = redis.Redis(host='redis', port=6379, db=0)



@shared_task
def crawl(cursor=0):
    tree = BKTree()
    print("...Started crawling...")
    url_objects = URLs.objects.filter(id__gt=cursor).order_by("id")
    links = list(url_objects.values("id", "url"))
    last_id = '0'
    while len(links) > 0 and int(last_id) <= 300000:
        links = list(url_objects.values("id", "url"))
        last_id = links[-1]["id"]
        with ThreadPoolExecutor(max_workers=int(os.environ.get("MAX_THREADS", 10))) as executor:
            results = executor.map(scrape_page, links)

        for result in results:
            for url in result:
                try:
                    URLs.objects.create(url=url)
                except Exception as e:
                    print(f'ERROR {e}')

        keys = r.scan_iter("crawler_*")
        for key in keys:
            word_str = key.decode().replace("crawler_", "")
            print(f'WORD STR = {word_str}')
            try:
                url_ids = list(map(int, r.lrange(key, 0, -1)))
                word_obj, _ = Word.objects.get_or_create(word=word_str)
                word_urls = [
                    WordURL(word=word_obj, url_id=int(url_id))
                    for url_id in url_ids
                ]
                WordURL.objects.bulk_create(word_urls, ignore_conflicts=True)
                r.delete(key)
                tree.add(word_str)
            except Exception as e:
                print(f"Error occurred while storing URL-Word pair {e}")
        url_objects = URLs.objects.filter(id__gt=last_id).order_by("id")
        links = list(url_objects.values("id", "url"))
    print('completed scraping')
    tree.save(f"{os.environ.get('WORD_DICT_NAME')}.pkl")
    print('storing word -> id map i db')
    del tree


@shared_task
def gen_tree():
    tree = BKTree()
    all_words = Word.objects.all()
    for w in all_words:
        tree.add(w.word)
        print(w.word)
    tree.save(f"{os.environ.get('WORD_DICT_NAME')}.pkl")
    print("tree built completely")
    del tree






