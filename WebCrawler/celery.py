import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WebCrawler.settings')

app = Celery('WebCrawler')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

#
# app.conf.beat_schedule = {
#     'add-every-30-seconds': {
#         'task': 'bk_tree_manager.tasks.crawl',
#         'schedule': 3600.0,
#         # 'args': (16, 16)
#     },
# }


app.conf.timezone = 'UTC'


