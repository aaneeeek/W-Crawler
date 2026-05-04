import os
from concurrent.futures import ThreadPoolExecutor
from celery import shared_task
from .models import URLs, Word, WordURL
from .scrapper import scrape_page
from .serializers import URLSerializer
from .bk_tree import BKTree
# import ssdb
#
# r = ssdb.SSDB(host='ssdb', port=8888)

import redis

r = redis.Redis(host='redis', port=6379, db=0)


@shared_task
def crawl(cursor=0):
    print("...Started crawling...")
    url_objects = URLs.objects.filter(id__gt=cursor).order_by("id")
    links = list(url_objects.values("id", "url"))
    last_id = '0'
    while len(links) > 0 and int(last_id) <= 800:
        links = list(url_objects.values("id", "url"))
        last_id = links[-1]["id"]
        if int(last_id) >= 200:
            break

        with ThreadPoolExecutor(max_workers=int(os.environ.get("MAX_THREADS", 10))) as executor:
            results = executor.map(scrape_page, links)

        for result in results:
            for url in result:
                try:
                    URLs.objects.create(url=url)
                except Exception as e:
                    print('ERROR')
        url_objects = URLs.objects.filter(id__gt=last_id).order_by("id")
        links = list(url_objects.values("id", "url"))

    print('completed scraping')
    keys = r.scan_iter("*")
    for key in keys:
        word_str = key.decode()
        print(f'WORD STR = {word_str}')
        try:
            url_ids = list(map(int, r.lrange(word_str, 0, -1)))
            word_obj, _ = Word.objects.get_or_create(word=word_str)
            word_urls = [
                WordURL(word=word_obj, url_id=int(url_id))
                for url_id in url_ids
            ]
            WordURL.objects.bulk_create(word_urls, ignore_conflicts=True)
        except:
            pass
    try:
        print('Started building tree')
        tree = BKTree()
        tree.build(list(keys))
        print('Tree building complete')
        tree.save(f"{os.environ.get('WORD_DICT_NAME')}.pkl")
        print('storing word -> id map i db')
    except Exception as e:
        print(e)






