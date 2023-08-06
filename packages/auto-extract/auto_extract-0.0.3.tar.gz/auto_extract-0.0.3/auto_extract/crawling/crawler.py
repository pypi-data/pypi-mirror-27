import time
import requests
import lxml.html
from auto_extract import Article
from auto_extract.utils import extract_domain
from auto_extract.crawling.storage import Storage
from auto_extract.crawling.regexes import make_regex


class Crawler(object):
    def __init__(self, seed_url, name,
                 all_required_regexes=None,
                 any_exclude_regexes=None,
                 base_url=None,
                 url_xpath="//a/@href",
                 remove_query_param=True,
                 item_class=Article.from_url,
                 get_id=lambda x: x,
                 send_mail=lambda articles, project_name: None,
                 add_query_param_nonce=False):
        self.seed_url = seed_url
        self.storage = Storage(name, send_mail=send_mail)
        self.name = name
        self.domain, _ = extract_domain(seed_url)
        self.base_url = base_url or seed_url
        all_required_regexes = all_required_regexes or []
        self.all_required_regexes = [make_regex(x) for x in all_required_regexes]
        any_exclude_regexes = any_exclude_regexes or []
        self.any_exclude_regexes = [make_regex(x) for x in any_exclude_regexes]
        self.url_xpath = url_xpath
        self.remove_query_param = remove_query_param
        self.get_id = get_id
        self.s = requests.Session()
        self.add_query_param_nonce = add_query_param_nonce

    def get(self, url):
        return self.s.get(url, headers={'User-Agent': 'Mozilla/5.0 ;Windows NT 6.1; WOW64; Trident/7.0; rv:11.0; like Gecko'})

    def pre_process_url(self, url):
        if self.remove_query_param:
            url = url.split("?")[0]
        return url

    def view_tree(self):
        from requests_viewer import view_tree
        view_tree(lxml.html.fromstring(self.get(self.seed_url).content))

    def return_seed_url_with_query_nonce(self):
        semi_random_nonce = str(int(time.time()))
        separator = "&" if "?" in self.seed_url else "?"
        return self.seed_url + separator + "additionals_param=" + semi_random_nonce

    def get_links(self):
        seed_url = self.return_seed_url_with_query_nonce() if self.add_query_param_nonce else self.seed_url
        tree = lxml.html.fromstring(self.get(self.seed_url).content)
        tree.make_links_absolute(self.domain)
        links = {}
        for link in tree.xpath(self.url_xpath):
            link = self.pre_process_url(link)
            if not link.startswith(self.base_url):
                continue
            if link in self.seed_url:
                continue
            if self.any_exclude_regexes and any([x.search(link) for x in self.any_exclude_regexes]):
                continue
            if self.all_required_regexes and not all([x.search(link) for x in self.all_required_regexes]):
                continue
            link_id = self.get_id(link)
            if link_id not in self.storage.seen:
                self.storage.seen.add(link_id)
                links[link_id] = link
        return links

    def save_articles_from_links(self, links):
        articles = []
        for link_id, link in links.items():
            article = Article.from_url(link)
            article.id = link_id
            articles.append(article)
        self.storage.add_articles(articles)

    def start(self):
        self.save_articles_from_links(self.get_links())
