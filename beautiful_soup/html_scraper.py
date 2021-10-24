import httplib2
import os
from bs4 import BeautifulSoup, SoupStrainer


http_obj = httplib2.Http(".cache", disable_ssl_certificate_validation=True)

urls = ['https://quotes.toscrape.com/page/1/',
        'https://quotes.toscrape.com/page/2/']

with open('quotes.json', 'a+', encoding='utf-8') as f:
    f.write('[')
    f.write('\n')

for i, url in enumerate(urls):

    try:
        status, response = http_obj.request(url)
    except:
        status = {'status': '400'}

    if status['status'] == '200':

        with open('quotes.json', 'a+', encoding='utf-8') as f:
            if (i > 0):
                f.write(',\n')

        for j, quote_block in enumerate(BeautifulSoup(response, parse_only=SoupStrainer('div', class_='quote'), features='html.parser')):

            quote_text = quote_block.find('span', class_='text').string
            author = quote_block.find('small', class_='author').string
            tags = []
            for a_tag in quote_block.find_all('a', class_='tag'):
                tags.append(a_tag.string)

            with open('quotes.json', 'a+', encoding='utf-8') as f:
                if (j > 0):
                    f.write(',\n')
                json_object = f'{{\"text\":\"{quote_text}\", \"author\":\"{author}\", \"tags\":\"{tags}\"}}'
                f.write(json_object)


with open('quotes.json', 'a+', encoding='utf-8') as f:
    f.write('\n]')
