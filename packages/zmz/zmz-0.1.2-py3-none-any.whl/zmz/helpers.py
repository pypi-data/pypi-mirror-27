import pickle
from prettytable import PrettyTable


class Helper:

    @staticmethod
    def db_save(articles: dict, area: str):
        db = open('./data/' + area + '_article.db', 'wb')
        pickle.dump(articles, db)

    @staticmethod
    def db_load(area: str):
        db = open('./data/' + area + '_article.db', 'rb')
        return pickle.load(db)

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
            table.add_row([article.resource_id, article.update_time, article.title, article.point])
        print(table)

    @staticmethod
    def print_download_links(articles, resource_id):
        articles[resource_id].print_download_links(True)

