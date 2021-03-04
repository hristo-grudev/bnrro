import scrapy

from scrapy.loader import ItemLoader
from ..items import BnrroItem
from itemloaders.processors import TakeFirst


class BnrroSpider(scrapy.Spider):
	name = 'bnrro'
	start_urls = ['https://www.bnr.ro/Noutati-584.aspx']

	def parse(self, response):
		post_links = response.xpath('//span[@class="list_header"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//div[@id="contentDiv"]/h2/text()|//h1/text()').get()
		description = response.xpath('//div[@class="com"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="data_com"]/text()').get()

		item = ItemLoader(item=BnrroItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
