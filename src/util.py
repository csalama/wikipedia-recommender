import xml.sax
import requests
from bs4 import BeautifulSoup
from gensim.corpora.wikicorpus import filter_wiki
from gensim.parsing.preprocessing import preprocess_string
import re

class WikiXmlHandler(xml.sax.handler.ContentHandler):
    """Content handler for Wiki XML data using SAX"""
    def __init__(self):
        xml.sax.handler.ContentHandler.__init__(self)
        self._buffer = None
        self._values = {}
        self._current_tag = None
        self._article_count = 0
        self._pages = []
        self._titles = []

    def characters(self, content):
        """Characters between opening and closing tags"""
        if self._current_tag:
            self._buffer.append(content)

    def startElement(self, name, attrs):
        """Opening tag of element"""
        if name in ('title', 'text'):
            self._current_tag = name
            self._buffer = []

    def endElement(self, name):
        """Closing tag of element"""
        if name == self._current_tag:
            self._values[name] = ' '.join(self._buffer)

        if name == 'page':
            #Check if there are more than 800 total characters (including wiki text) in the article (long article)
            if len(self._values['text'])>800:
                self._article_count += 1
                article_sentences = cleanWiki(self._values['text'])
                self._pages.append(article_sentences)
                self._titles.append(self._values['title'])

def cleanWiki(raw_text):
    c_1 = filter_wiki(raw_text.replace('\n','').strip())
    c_2 = re.sub(r'^thumb\|[^|]*\|?','',c_1)
    c_3 = c_2.split('=',1)[0]
    return preprocess_string(c_3)
