import os
from concurrent.futures import ThreadPoolExecutor
from celery import shared_task
from bk_tree_manager.bk_tree import BKTree
from itertools import repeat
from connection.db_connection import PostgresDBConnector, MySQLDBConnector
from connection.utils import scrape_url, get_content
from searcher.utils import arrange_words, get_result


@shared_task
def search(client_app):
    search_sentence = client_app.prompt
    key_words = arrange_words(search_sentence)
    print(key_words)
    tree = BKTree.load(f"{os.environ.get('WORD_DICT_NAME')}.pkl")
    with ThreadPoolExecutor(max_workers=int(os.environ.get("MAX_THREADS", 10))) as executor:
        results = executor.map(get_result, key_words, repeat(tree))

    print(results)
    for result_set in results:
        for result in result_set:
            text = get_content(result["url_obj"]["url"])
            sql_commands = scrape_url(text, client_app.queries, client_app.tables, client_app.prompt)
            if client_app.db_type == 'mysql':
                pg_connector = PostgresDBConnector(
                    client_app.db_name, client_app.db_host,
                    client_app.db_user, client_app.db_password, client_app.port
                )
                for command in sql_commands:
                    pg_connector.insert(command)
            else:
                mysql_connector = MySQLDBConnector(
                    client_app.db_name, client_app.db_host,
                    client_app.db_user, client_app.db_password, client_app.port
                )
                for command in sql_commands:
                    mysql_connector.insert(command)




