# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['lagou.com']
    start_urls = ['https://www.lagou.com/beijing-zhaopin/Python/?labelWords=label']

    rules = (
        # 抓取详细数据
        # Rule(LinkExtractor(allow=r'jobs/\d+\.html'), callback='parse_item'),

        # 实现翻页
        Rule(LinkExtractor(allow=r'beijing-zhaopin/Python/\d+/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # todo:使用抓取详细数据的Rule
        # item = {}
        # # item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        # # item['name'] = response.xpath('//div[@id="name"]').get()
        # # item['description'] = response.xpath('//div[@id="description"]').get()
        # item['title'] = response.xpath('/html/body/div[6]/div/div[1]/div/h1/text()').extract_first()
        # item['company'] = response.xpath('//*[@id="job_company"]/dt/a/div/h3/em/text()').extract_first()
        # # item['working_location'] = response.css('body > div.position-head > div > div.position-content-l > dd > h3 > span:nth-child(2):text').extract_first()
        # # item['acquire'] = response.css('#job_detail > dd.job_bt > div > p:nth-child(11):text').extract_first()
        # # item['company'] =response.css('#job_company > dt > a > div > h3 > em:text').extract_first()
        # print(item)

        # 获取当页的每个li的职位相关信息
        ul_list = response.xpath('//*[@id="s_position_list"]/ul')
        for li in ul_list:
            item = {}
            item['title'] = li.css('.con_list_item::attr(data-positionname)').extract_first()
            item['company'] = li.css('.con_list_item::attr(data-company)').extract_first()
            item['salary'] = li.css('.con_list_item::attr(data-salary)').extract_first()
            item['href'] = li.css('.position_link::attr(href)').extract_first()

            yield scrapy.Request(
                item['href'],
                callback=self.parse_detail,
                meta={'item': item}
            )

    def parse_detail(self, response):
        item = response.meta['item']
        item['content'] = response.xpath('//*[@id="job_company"]/dd/ul/li[5]/a/@href').extract_first()
        print(item)
        yield item
