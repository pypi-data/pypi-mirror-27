import os
import just


class Storage():
    def __init__(self, project_name, send_initially=False, mail=True, root="~/.tradex",
                 send_mail=lambda articles, project_name: None):
        self.root = root
        self.project_name = project_name
        self._articles = None
        self._seen = None
        self.mail = mail
        self.send_initially = send_initially
        self.send_mail = send_mail

    def __len__(self):
        return len(self.seen)

    def __repr__(self):
        return '{}(path="{}", num_articles={})'.format(self.__class__.__name__, self.path, len(self))

    @property
    def path(self):
        return os.path.join(self.root, self.project_name)

    @property
    def index_path(self):
        return os.path.join(self.path, "index.jsonl")

    @property
    def articles_path(self):
        return os.path.join(self.path, "articles.jsonl")

    def add_articles(self, articles):
        if articles:
            print("{} new articles in {}".format(len(articles), self.project_name))
            if self.mail and (self.send_initially or self.seen):
                print("emailing!")
                self.send_mail(articles, self.project_name)
        for article in articles:
            just.append(article.id, self.index_path)
            # self.seen.add(self.get_id(article))
            self.articles.append(article.to_dict())
            just.append(article, self.articles_path)

    @property
    def seen(self):
        if self._seen is None:
            self._seen = set(just.iread(self.index_path, no_exist=[]))
        return self._seen

    @property
    def articles(self):
        if self._articles is None:
            self._articles = list(just.iread(self.articles_path, no_exist=[]))
        return self._articles

    def clear(self):
        just.remove(self.path, recursive=True)
        self._seen = None
        self._articles = None
        print("Removed {}".format(self.path))

    def drop_one(self):
        article_id = self._seen.pop()
        if self._articles is not None:
            self._articles = [x for x in self._articles if x.id != article_id]
