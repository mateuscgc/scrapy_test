import scrapy


class TagsSpider(scrapy.Spider):
    name = "tags"

    quotes_by_tag = {}

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):

        for quote in response.css('.quote'):
            for tag in quote.css('.tags .tag::text').extract():
                if not tag in self.quotes_by_tag:
                    self.quotes_by_tag[tag] = 1
                else:
                    self.quotes_by_tag[tag] += 1

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse)
        else:
            for tag in self.quotes_by_tag:
                yield { tag: self.quotes_by_tag[tag] }

