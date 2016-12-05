import lxml.html
import requests
import re
import pandas as pd
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import RussianStemmer
from stop_words import get_stop_words

add = 'http://www.gazeta.ru'
tags = ['politics', 'business', 'social', 'army', 'culture', 'science', 'tech', 'auto', 'lifestyle']
# tags = ['politics']
data = pd.DataFrame(columns=('tag', 'url', 'title', 'text', 'tokens'))


tokenizer = RegexpTokenizer(r'[а-я]+')
stop_words = get_stop_words('ru')
stemmer = RussianStemmer()


def parse(text):
    line = text.strip().lower()
    raw_tokens = tokenizer.tokenize(line)
    stopped_tokens = [i for i in raw_tokens if (not i in stop_words) and (len(i) > 2)]
    stemmed_tokens = [stemmer.stem(i) for i in stopped_tokens]
    return ' '.join(stemmed_tokens)


def get_text(url):
    response = requests.get(add + url)
    if response.status_code == 200:
        tree = lxml.html.fromstring(response.text)
        text = ' '.join(tree.xpath('//div[@class="article_text txt_1"]/p/text()'))
        title = tree.xpath('//h2[@class="h_1 mt5 mb10"]/text()')
        if title:
            title = title[0]
        else:
            title = ''
        print(title)
        parsed_text = parse(text)
        # print(text)
        return title, text, parsed_text
    else:
        print(response.status_code)
        print(url)
        exit(0)


if __name__ == "__main__":
    i = 0
    with open('gazeta_articles.csv', 'w') as f:
        for tag in tags:
            urls = []
            print(tag)
            next_page = '{0}/{1}/'.format(add, tag)
            year16 = re.compile('/2016/')
            year15 = re.compile('/2015/')
            while (True):
                response = requests.get(next_page)
                if response.status_code == 200:
                    tree = lxml.html.fromstring(response.text)
                    urls += tree.xpath('//div[@class="tile_inner_size"]/a/@href')
                    next = tree.xpath('//a[@id="other_clickA"]/@href')
                    if(next):
                        next_page = add+tree.xpath('//a[@id="other_clickA"]/@href')[0]
                    else:
                        break
                    print(len(urls))
                    if (not year16.search(urls[-1])) and (not year15.search(urls[-1])):
                        break
                else:
                    print(response.status_code)
                    print(next_page)
                    exit(0)
            for url in urls:
                print(url)
                title, text, parsed_text = get_text(url)
                data.loc[len(data)] = [tag, url, title, text, parsed_text]
        data.to_csv('gazeta_articles.csv')