# -*- coding: utf-8 -*-
import scrapy
import json

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem


class Brasil247Spider(scrapy.Spider):
    name = 'brasil_247'
    allowed_domains = ['brasil247.com']
    start_urls = []

    visited_urls = []

    def __init__(self, *a, **kw):
        super(Brasil247Spider, self).__init__(*a, **kw)
        with open('seeds/brasil_247.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())

    def parse(self, response):
        '''
            Percorre as notícias da main-page, passando para o método encarregado de extrair as informacoes da página da notícia
        '''
        for article in response.css('section.section-column'):
            links = article.css('h3 a::attr(href)').extract()
            for link in links:
                yield response.follow(link, self.parse_article)

        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)


    '''
    Método encarregado de fazer o parser de cada página de notícia
    '''
    def parse_article(self, response):
        '''
        Inclui a url na lista de urls visitadas, para evitar duplicacao 
        '''
        self.visited_urls.append(response.url)

        related_links = response.css('div.aside-box article a::attr(href)').extract()

        article_link = response.url
        title = response.css('div.featured-box h1::text').extract_first()
        subtitle = response.css('div.featured-box p::text').extract_first()
        date = response.css('div.featured-box p::text').extract()[1]
        author = response.css('section p strong *::text').extract_first().replace("-", "")
        text = " ".join(response.css('section p *::text').extract())
        
        section_actor_end = text.find('-') + 1

        text = text[section_actor_end:]

        section_url_begin = article_link.find('/247/') + 5
        section_url_end = article_link.index('/', section_url_begin)
        section = article_link[section_url_begin:section_url_end]

        item = RiLab01Item(title=title.strip(), sub_title=subtitle.strip(), author=author.strip(), date=date.strip(), url=article_link, text=text.strip(), section=section)

        print(item)

        '''
        Visita os links em "Matérias relacionadas"
        '''
        for link in related_links:
            if link not in self.visited_urls:
                print(link)
                yield response.follow(link, self.parse_article)
        
        yield item
