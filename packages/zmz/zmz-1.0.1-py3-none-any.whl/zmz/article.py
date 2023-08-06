import re
import requests
from threading import Thread
from datetime import datetime
from bs4 import BeautifulSoup

# Request links
home_page = 'http://www.zimuzu.tv'
base_link = 'http://www.zimuzu.tv/resourcelist'
resource_page = 'http://www.zimuzu.tv/resource/index_json/rid/'
channel_link = '/channel/tv'

# Area links
us_area = '美国'
uk_area = '英国'
jp_area = '日本'


class Article:

    def __init__(self, article_id, resource_link, update_time, title, point):
        self.article_id = article_id
        self.resource_link = resource_link
        self.update_time = update_time
        self.title = title
        self.point = point
        self.download_links = []

    @staticmethod
    def get_articles_by(area, pages):
        articles_dict = {}
        article_list_soups = []

        # Request html by page
        def get_article_list_soups(area_str, page):
            params = {'channel': 'tv', 'area': '', 'page': ''}

            # Setting area
            if area_str == 'jp':
                params['area'] = jp_area
            elif area == 'us':
                params['area'] = us_area
            elif area == 'uk':
                params['area'] = uk_area

            # Setting page
            params['page'] = page

            # Parse html
            article_soup = BeautifulSoup(requests.get(base_link, params=params).text, 'lxml')
            article_list_soups.append(article_soup)
        threads = [Thread(target=get_article_list_soups, args=(area, page,)) for page in range(1, pages + 1)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Parse all soup to article object
        for soup in article_list_soups:
            # Find articles div
            articles_div = soup.find('div', class_='resource-showlist has-point').ul

            # Find every article div
            article_div_list = articles_div.find_all('li', class_='clearfix', recursive=False)

            # Parse every article
            for article in article_div_list:
                # Resource id
                article_id = article.div.a['href'].split('/')[-1]

                # Resource link
                resource_link = resource_page + article_id + channel_link

                # Update time
                update_time = article.find('span', class_='fr f3 dateline')['time']
                update_time = datetime.fromtimestamp(int(update_time))

                # Article title
                title = article.find('div', class_='fl-info').dl.dt.h3.a.text
                title = re.findall(r'《(.+)》', title)[0]

                # Article ranking point
                point = article.find('span', class_='point').text

                # Add to dict
                articles_dict[article_id] = Article(article_id, resource_link, update_time, title, point)

        return articles_dict

    def _get_download_links(self):
        # Get download page link
        json = requests.get(self.resource_link)
        soup = BeautifulSoup(json.text.replace('\\', ''), 'lxml')
        link = soup.find('h3').a['href']
        if not link.count('xiazai'):
            return None

        # Parse download links
        response = requests.get(link)
        if response.status_code == 404:
            return None
        soup = BeautifulSoup(response.text, 'lxml')

        # Parse seasons
        seasons = []
        seasons_box = soup.find('div', class_='col-box col-sidebar').div.ul
        seasons_list = seasons_box.find_all('li', recursive=False)
        seasons_titles = []
        for season in seasons_list:
            seasons_titles.append(season.a.text)

        # Parse episodes in each seasons
        seasons_box = soup.find('div', class_='tab-content info-content')
        seasons_divs = seasons_box.find_all('div', recursive=False)
        for seasons_title, seasons_div in zip(seasons_titles, seasons_divs):
            episodes_boxes = seasons_div.div.find_all('div', recursive=False)

            # Find best video type
            video_types = [episodes_box['id'].split('-')[-1] for episodes_box in episodes_boxes]
            index = 0
            video_type = ''
            while video_types[index] == 'APP':
                if len(video_types) == 1:
                    video_type = 'APP'
                    break
                index += 1
            episodes_ul = episodes_boxes[index].ul
            episodes_list = episodes_ul.find_all('li', recursive=False)

            # Parse episodes
            episodes = []
            for episode in episodes_list:
                # Episode title
                title = episode.div.span.text.split(' ')[-1]

                # Episode download link
                link_li = episode.ul.find('li')
                if link_li is None:
                    link = ''
                else:
                    if video_type == 'APP':
                        link = link_li.a['data-url']
                    else:
                        link = link_li.a['href']

                # Add to episodes list
                episodes.append(Episode(title, link))

            # Add to seasons list
            seasons.append(Season(seasons_title, episodes))

        return seasons

    def print_download_links(self, is_links_only):
        seasons = self._get_download_links()
        print(self.title)
        if seasons is None:
            print('[没有下载链接]')
            return
        for season in seasons:
            print(season.to_str(is_links_only))


class Season:

    def __init__(self, title, episodes):
        self.title = title
        self.episodes = episodes

    def to_str(self, is_links_only):
        season_info = ''
        season_info += ('-' * 2 * len(self.title)) + '\n'
        season_info += self.title + '\n'
        season_info += ('-' * 2 * len(self.title)) + '\n'
        for episode in self.episodes:
            season_info += episode.to_str(is_links_only) + '\n'
        return season_info


class Episode:

    def __init__(self, title, link):
        self.title = title
        self.link = link

    def to_str(self, is_links_only):
        if is_links_only:
            return self.link
        else:
            return '[' + self.title + ']\n' + self.link
