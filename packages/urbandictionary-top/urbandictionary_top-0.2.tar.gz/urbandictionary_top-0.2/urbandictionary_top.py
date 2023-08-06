'''
A dead-simple module that fetches the top definition
of a term from urbandictionary.
'''

from urllib.parse import quote
import requests
from bs4 import BeautifulSoup


class udtop:
    '''
    An entry in urbandictionary.
    '''

    class TermNotFound(Exception):
        '''
        Error that is raised when a term is not found in urbandictionary.
        '''
        def __init__(self, term):
            Exception.__init__(self, term + ' not found in urbandictionary!')

    def __init__(self, keyword):
        url = ('https://www.urbandictionary.com/define.php?term={}'
               .format(quote(keyword)))
        raw = requests.get(url).text
        soup = BeautifulSoup(raw, 'html5lib')
        top = soup.find(class_="meaning").text
        if "There aren't any definitions for {} yet.".format(keyword) in top:
            raise self.TermNotFound(keyword)
        self.definition = top.strip()
        self.example = soup.find(class_="example").text.strip()

    def __str__(self):
        if self.example:
            return self.definition + '\n\nExample:\n' + self.example
        return self.definition

    def __repr__(self):
        return str(self)
