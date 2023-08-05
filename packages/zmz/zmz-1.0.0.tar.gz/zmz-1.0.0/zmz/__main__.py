import click
from zmz.article import Article
from zmz.helpers import Helper


@click.group()
def main():
    pass


@click.command()
@click.option('-a', '--area', type=click.Choice(['jp', 'us', 'uk']), help='The area you want to show.')
@click.option('-p', '--pages', type=int, default=1, help='Number of pages.')
def show(area, pages):
    """Show articles table."""
    if area is None:
        click.echo('The area option must be inputted.')
        click.echo('Use [--help] for more information.')
        return

    articles = Article.get_articles_by(area=area, pages=pages)
    Helper.print_article_by_update_time(articles)
    Helper.db_save(articles)


@click.command()
@click.option('-i', '--article_id', type=str, help='The article ID.')
def get(article_id):
    """Get article download links by ID."""
    if article_id is None:
        click.echo('The article id option must be inputted.')
        click.echo('Use [--help] for more information.')
        return

    articles = Helper.db_load('articles')
    if articles is None:
        click.echo('There is no any article in your database.')
        click.echo('Use [show] command to get some. :)')
        return

    Helper.print_download_links(articles, article_id, False)


# add command to group
main.add_command(show)
main.add_command(get)


if __name__ == "__main__":
    main()
