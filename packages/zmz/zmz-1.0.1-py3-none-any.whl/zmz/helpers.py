import os
import errno
import pickle
from prettytable import PrettyTable


class Helper:

    @staticmethod
    def db_save(articles: dict):
        # Check if db directory is exists.
        try:
            os.makedirs('~/.data')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        # Check if db file is exists
        db_path = '~/.data/articles.db'
        db = open(db_path, 'wb')
        if os.path.exists(db_path):
            new_articles = articles
        else:
            old_articles = pickle.load(db)
            new_articles = {**articles, **old_articles}

        # Update articles db and save
        pickle.dump(new_articles, db)

    @staticmethod
    def db_load(db_type: str):
        # Load db file and return articles dict
        db_path = '~/.data/'
        if os.path.exists(db_path):
            db = open(db_path + db_type + '.db', 'rb')
            return pickle.load(db)
        else:
            return None

    @staticmethod
    def print_article_by_update_time(articles: dict, reverse=True):
        articles_list = sorted(articles.values(), key=lambda x: x.update_time, reverse=reverse)
        Helper.print_table(articles_list)

    @staticmethod
    def print_article_by_point(articles: dict, reverse=True):
        articles_list = sorted(articles.values(), key=lambda x: x.point, reverse=reverse)
        Helper.print_table(articles_list)

    @staticmethod
    def print_table(articles: list):
        print('合计', len(articles), '部剧')
        table = PrettyTable(['ID', '更新时间', '名称', '评分'])
        for article in articles:
            table.add_row([article.article_id, article.update_time, article.title, article.point])
        print(table)

    @staticmethod
    def print_download_links(articles, article_id, is_link_only):
        articles[article_id].print_download_links(is_link_only)

