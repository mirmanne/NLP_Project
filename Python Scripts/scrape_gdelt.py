#!/usr/bin/env python3
import argparse
import logging
import json
from newspaper import Article, ArticleException, Config
import sys
import traceback

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(levelname)s: %(asctime)s: %(message)s')
handler.setFormatter(formatter)
#logger.addHandler(handler)


class GdeltArticle:
    """An Article class encapsulates download and metadata functionality"""

    def __init__(self, url):
        self.url = url
        self.config = Config()
        self.config.memoize_articles = False
        #self.config.fetch_images = False
        self.config.browser_user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.35 Safari/537.36'
        self.config.request_timeout = 30
   
        #logger.info('url is %s', url)
        self.article = Article(url, config=self.config)
        self._import_article()

        self.results = {}
        self.results['sourceurl'] = url
        try:
            self.results['title'] = self.article.title
            self.results['authors'] = self.article.authors
            self.results['canonical_link'] = self.article.canonical_link
            self.results['url'] = self.article.url
            self.results['top_image'] = self.article.top_image
            self.results['images'] = list(self.article.images)
            self.results['movies'] = self.article.movies
            self.results['description'] = self.article.meta_description
            #self.results['meta_favicon'] = self.article.meta_favicon
            self.results['keywords'] = self.article.meta_keywords
            self.results['lang'] = self.article.meta_lang
            self.results['summary'] = self.article.summary
            self.results['tags'] = list(self.article.tags)
            self.results['text'] = self.article.text
        except Exception:
            logger.fatal('Unable to make results for:%s, %s', url, results)
            pass
        
    def _import_article(self):
        try:
            self.article.download()
        except ArticleException:
            logger.warning('Unable to download: %s', self.url)
            return 1
        try:
            self.article.parse()
        except Exception as ex:
            logger.warning('Unable to parse %s', self.url)
            logger.debug(repr(ex))
            return 2

    def print_results(self):
        try:
            print(json.dumps(self.results))
            sys.stdout.flush()
        except OSError:
            logger.fatal('output stream unavailable: %s', ex)
            return 3
        except Exception as ex:
            logger.fatal('Unable to serialize: %s', ex)
            return 1


def main(url):
    article = GdeltArticle(url)
    article.print_results()
    logger.info("SUCCESS: %s", url)
    return 0


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument(
        '--url',
        type=str,
        help='The page to search for images')
    ARGS = PARSER.parse_args()
    RET = main(ARGS.url)
    sys.exit(RET)
