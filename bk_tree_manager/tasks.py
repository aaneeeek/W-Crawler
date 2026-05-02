import os
from concurrent.futures import ThreadPoolExecutor
from celery import shared_task
from .models import URLs
from .scrapper import scrape_page
from .serializers import URLSerializer
from .bk_tree import BKTree
import redis

r = redis.Redis(host='redis', port=6379, db=0)


@shared_task
def crawl(cursor=0):
    if cursor == 0:
        print("...Started crawling...")
    url_objects = URLs.objects.filter(id__gt=cursor).order_by("id")
    if url_objects.exists():
        links = URLSerializer(url_objects, many=True).data
        last_id = links[-1]["id"]
        with_recursion = False
        with ThreadPoolExecutor(max_workers=int(os.environ.get("MAX_THREADS", 10))) as executor:
            results = executor.map(scrape_page, links)
        for result in results:
            for url in result:
                try:
                    URLs.objects.create(url=url)
                    with_recursion = True
                except:
                    pass
        if with_recursion:
            crawl.delay(last_id)
    else:
        print('completed scraping')
        tree = BKTree()
        keys = [k.decode() for k in r.scan_iter("*")]
        tree.build(keys)
        tree.save(f"{os.environ.get('WORD_DICT_NAME')}.pkl")





