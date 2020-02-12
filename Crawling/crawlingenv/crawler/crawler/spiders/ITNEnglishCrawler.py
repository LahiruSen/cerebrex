import scrapy
import json
import io
from pathlib import Path
from random import randrange

class ITNEnglishCrawler(scrapy.Spider):
    name = "ITNEnglishCrawler"

    data = {}
    data['news'] = []

    start_urls = [
        'https://www.itnnews.lk/en/local/',
        'https://www.itnnews.lk/en/international/',
        'https://www.itnnews.lk/en/business/',
        'https://www.itnnews.lk/en/sports/',
        'https://www.itnnews.lk/en/entertainment/'
    ]

    def writeToJson(self, header, time, content):
        obj = {  
            'Header': header,
            'Time': time,
            'Content': content
        }

        Path("./data/itn/english").mkdir(parents=True, exist_ok=True)
        with open("./data/itn/english/" + time + str(randrange(1000000)) + ".json", 'a', encoding="utf8") as outfile:  
            json.dump(obj, outfile, ensure_ascii=False)

    def parse(self, response):
        for link in response.css('div.block-content a.more ::attr(href)').getall():
            if link is not None:
                yield scrapy.Request(response.urljoin(link), callback = self.parseNews)
        yield scrapy.Request(response.css('a.next ::attr(href)').get(), self.parse)

    def parseNews(self, response):
        header = response.css("div.article-title h1 ::text").get()
        content = response.css("div.column9 ::text").getall()
        time = response.css('div.a-content span.meta ::text').get()
        self.writeToJson(header, time, content)
