import scrapy

class Crawler(scrapy.Spider):
	name='spider-repositories'
	def start_requests(self):
		url = 'https://github.com/shiyanlou?page={}&tab=repositories'
		urls = (url.format(i) for i in range(1, 5))

		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		for repository in response.css('li.col-12'):
			yield {
				'name':repository.css('a::text').re_first('[^\w]*(.*)[^\w]*'),
				'update_time':repository.css('relative-time::attr(datetime)').extract_first()
			}
