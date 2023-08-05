import click
from zmz.article import Article
from zmz.helpers import Helper


@click.group()
def main():
    pass


@click.command()
@click.option('-a', '--area', type=str, help='The area you want to show. (jp, us, uk)')
@click.option('-p', '--pages', default=1, help='Number of pages.')
def show(area, pages):
    """Show articles."""
    articles = Article.get_articles_by(area=area, pages=pages)
    Helper.print_article_by_update_time(articles)
    Helper.db_save(articles, area=area)


# add command to group
main.add_command(show)


if __name__ == "__main__":
    main()
