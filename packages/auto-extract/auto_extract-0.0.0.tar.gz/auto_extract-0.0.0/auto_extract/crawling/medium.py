from auto_extract.crawling.crawler import Crawler
from auto_extract.crawling.regexes import re_count


def remove_after_last_dash(article_url):
    return "-".join(article_url.split("-")[:-1])


class MediumCrawler(Crawler):

    def __init__(self, page):
        base_url = "https://medium.com/{}/".format(page)
        seed_url = base_url + "latest"
        super().__init__(base_url=base_url, seed_url=seed_url,
                         name="medium_{}".format(page),
                         any_exclude_regexes=["/about", "/archive",
                                              "/welcome", "/tagged", "/trending", "/@"],
                         all_required_regexes=[re_count("/", 4, 4)],
                         get_id=remove_after_last_dash)
        self.page = page
