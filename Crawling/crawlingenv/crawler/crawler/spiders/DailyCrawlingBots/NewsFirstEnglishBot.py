import scrapy
from pathlib import Path
from random import randrange
import json
import datetime

class NewsFirstEnglishBot(scrapy.Spider):
    name = "NewsFirstEnglishBot"

    start_urls = [
        'https://www.newsfirst.lk/latest-news/'
    ]
    oldSubLink = ""
    oldMainLink = ""

    def writeToJson(self, header, time, content, url):
        obj = {  
            'Header': header,
            'Time': time,
            'Url': url,
            'Content': content
        }

        Path("../../../data/news_first/bot/english").mkdir(parents=True, exist_ok=True)
        with open("../../../data/news_first/bot/english/" + str(randrange(1000000)) + ".json", 'a', encoding="utf8") as ofile:
            json.dump(obj, ofile, ensure_ascii=False)

    def parse(self, response):

        allnew = True

        newsLinks1 = response.css('div.sub-1-news-block ::attr(href)').getall()
        newsLinks2 = response.css('div.main-news-heading ::attr(href)').getall()
        
        yesterday = (datetime.date.today() + datetime.timedelta(days=-1)).strftime("%Y/%m/%d")

        if (len(newsLinks1) > 0 or len(newsLinks2) > 0):
            for link in newsLinks1:
                if link is not None and "2020/03/01" in link:
                    yield scrapy.Request(response.urljoin(link), callback = self.parseNews)
                    allnew = True
                else:
                    allnew = False
        
            for link in newsLinks2:
                if link is not None and "2020/03/01" in link:
                    yield scrapy.Request(response.urljoin(link), callback = self.parseNews)
                    allnew = True
                else:
                    allnew = False

            if (allnew):
                yield scrapy.Request(response.css('a.next ::attr(href)').get(), self.parse)
        else:
            yield scrapy.Request(response.css('a.next ::attr(href)').get(), self.parse)

    def parseNews(self, response):
        header = response.css("h1.text-left ::text").getall()
        content = response.css("div.w-300 p ::text").getall()
        time = response.css('p.artical-new-byline ::text').getall()[1:]
        url = response.url
        self.writeToJson(header, time, content, url)
