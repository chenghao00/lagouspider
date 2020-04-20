# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['lagou.com']
    start_urls = ['https://www.lagou.com/beijing-zhaopin/Python/?labelWords=label']

    rules = (
        Rule(LinkExtractor(allow=r'jobs/\d+\.html'), callback='parse_item'),
        Rule(LinkExtractor(allow=r'beijing-zhaopin/Python/\d+/'), follow=True),
    )

    def parse_item(self, response):
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        item['title'] = response.xpath('/html/body/div[6]/div/div[1]/div/h1/text()').extract_first()
        item['company'] = response.xpath('//*[@id="job_company"]/dt/a/div/h3/em/text()').extract_first()
        # item['working_location'] = response.css('body > div.position-head > div > div.position-content-l > dd > h3 > span:nth-child(2):text').extract_first()
        # item['acquire'] = response.css('#job_detail > dd.job_bt > div > p:nth-child(11):text').extract_first()
        # item['company'] =response.css('#job_company > dt > a > div > h3 > em:text').extract_first()
        print (item)
        return item
