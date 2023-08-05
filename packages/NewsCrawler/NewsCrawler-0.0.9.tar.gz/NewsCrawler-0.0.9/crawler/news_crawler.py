#!/usr/bin/env python3

import json
import urllib.request
import urllib.parse
import os
import datetime

import yaml
import ssl

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
TMP_PATH = "/tmp"


class NewsCrawler(object):
    """Retrieves article metadata from various sources"""

    def __init__(self):
        self.api_data = NewsCrawler.initialise_api()
        self.key = self.api_data["key"]
        self.url_template = self.api_data["url"]
        self.news_sources = self.get_news_sources()

    def __str__(self):
        return "Key: {0}\nURL Template: {1}".format(self.key, self.url_template)

    def load_articles(self):
        context = ssl._create_unverified_context()
        for source in self.news_sources:
            article_url = self.url_template.format(source)

            with urllib.request.urlopen(article_url, context=context) as url:
                data = json.loads(url.read().decode("UTF-8"))

            for article in data["articles"]:
                article_doc = "{0}/articledata/{1}.yaml".format(TMP_PATH, source)
                if os.path.exists(article_doc):
                    append_write = "a"
                else:
                    append_write = "w+"
                with open(article_doc, append_write) as source_yaml:
                    title = article["title"]
                    try:
                        desc = article["description"].encode("ascii", "ignore").decode("UTF-8")
                    except AttributeError:
                        print("Description unavailable for article " + title)
                        desc = ""
                    published = article["publishedAt"]
                    url = article["url"]

                    article_data = {
                        title: {
                            "description": desc,
                            "published": published,
                            "logged": str(datetime.datetime.now())[:-7].replace(" ", "T") + "Z",
                            "url": url
                        }
                    }

                    yaml.dump(article_data, source_yaml, default_flow_style=False)

    @staticmethod
    def initialise_api():
        api_data = {}
        with open(ROOT_DIR + "/config/config.yaml", "r") as config:
            config_stream = yaml.load(config)
            for conf_key in config_stream:
                if conf_key == "news_api":
                    for key in config_stream[conf_key]:
                        api_data[key] = config_stream[conf_key][key]

        return api_data

    @staticmethod
    def get_news_sources():
        sources = []
        with open(ROOT_DIR + "/config/config.yaml", "r") as config:
            config_stream = yaml.load(config)
            for conf_key in config_stream:
                if conf_key == "news_sources":
                    for source in config_stream[conf_key]:
                        sources.append(source)

        return sources


if __name__ == '__main__':
    nc = NewsCrawler()
    nc.load_articles()
