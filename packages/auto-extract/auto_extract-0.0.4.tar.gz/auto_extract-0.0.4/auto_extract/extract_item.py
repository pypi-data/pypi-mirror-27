import requests
from lxml.html import fromstring

import extruct

from auto_extract.utils import extract_domain
from auto_extract.utils import extract_links
from auto_extract.utils import extract_headings
from auto_extract.utils import lazy_property
from auto_extract.utils import get_full_text
from auto_extract.title import get_title
from auto_extract.title import get_title_index
from auto_extract.images import get_images
from auto_extract.language import get_language
from auto_extract.content import get_content


class Article():
    def __init__(self, response_body, response_url):
        self.response_body = response_body
        self.tree = fromstring(response_body)
        self.url = response_url
        self.id = response_url

    @lazy_property
    def title(self):
        return get_title(self.tree)

    @lazy_property
    def image(self):
        images = get_images(self.tree, self.url, get_title_index(self.tree, self.title))
        image = images[0] if images else ""
        return image

    @lazy_property
    def _date_and_article_text(self):
        return get_content(self.response_body, self.title, self.language, self.url)

    @property
    def publish_date(self):
        publish_date, _ = self._date_and_article_text
        return publish_date

    @property
    def article_text(self):
        _, article_text = self._date_and_article_text
        return article_text

    @lazy_property
    def domain(self):
        full_domain, _ = extract_domain(self.url)
        return full_domain

    @lazy_property
    def language(self):
        return get_language(self.tree)

    @lazy_property
    def full_text(self):
        return get_full_text(self.tree)

    @lazy_property
    def code(self):
        return [x.text_content() for x in self.tree.xpath("//code")]

    @lazy_property
    def links(self):
        return extract_links(self.tree, self.domain)

    @lazy_property
    def heading(self):
        return extract_headings(self.tree)

    @lazy_property
    def extruct(self):
        return extruct.extract(self.response_body)

    def __repr__(self):
        obj = {"title": self.title, "domain": self.domain,
               "url": self.url, "publish_date": self.publish_date}
        return "Article({})".format(obj)

    @classmethod
    def from_url(cls, url):
        response = requests.get(url)
        return cls(response.content, url)

    def to_dict(self, keys=("title", "publish_date", "url", "id", "article_text",
                            "extruct", "code", "links", "image")):
        return {x: getattr(self, x) for x in keys}


def parse_article(response_body, response_url):
    """ to be deprecated"""
    return Article(response_body, response_url)


def test_url(url):
    return extract_url(url)


def extract_url(url):
    response = requests.get(url)
    return parse_article(response.content, response.url)

# test_url("https://www.evmi.nl/mensen-en-bedrijven/has-hogeschool-start-minor-gericht-op-plantaardige-voeding/")
