# -*- coding: utf-8 -*-
import scrapy


class EbaySpider(scrapy.Spider):
	
	name = "ebay"
	allowed_domains = ["ebay.com"]
	start_urls = ["https://www.ebay.com"]

	# Allow a custom parameter (-a flag in the scrapy command)
	def __init__(self, search="hermes"):
		self.search_string = search

	def parse(self, response):
		# Extract the trksid to build a search request	
		trksid = response.css("input[type='hidden'][name='_trksid']").xpath("@value").extract()[0]       
		
		# Build the url and start the requests
		yield scrapy.Request("http://www.ebay.com/sch/i.html?_from=R40&_trksid=" + trksid +
							 "&_nkw=" + self.search_string.replace(' ','+') + "&_ipg=200", 
							 callback=self.parse_link)

	# Parse the search results
	def parse_link(self, response):
		# Extract the list of products 
		results = response.xpath('//li[@class="s-item   "]')
		
		# Extract info for each product
		for product in results:		
			name = product.xpath('.//*[@class="s-item__title"]//text()').extract_first()
			# Sponsored or New Listing links have a different class
			if name == None:
				name = product.xpath('.//*[@class="s-item__title s-item__title--has-tags"]/text()').extract_first()			
				if name == None:
					name = product.xpath('.//*[@class="s-item__title s-item__title--has-tags"]//text()').extract_first()			
			if name == 'New Listing':
				name = product.xpath('.//*[@class="s-item__title"]//text()').extract()[1]

			# If this get a None result
			if name == None:
				name = "ERROR"

			price = product.xpath('.//*[@class="s-item__price"]/text()').extract_first()
			status = product.xpath('.//*[@class="SECONDARY_INFO"]/text()').extract_first()
			link = product.xpath('.//a[@class="s-item__link"]/@href').extract_first()

			if product.xpath('.//*[@class="s-item__shipping s-item__logisticsCost"]/text()'):
				shipping = product.xpath('.//*[@class="s-item__shipping s-item__logisticsCost"]/text()').extract_first()
			else:
				shipping = 'Free Shipping'
		
			if product.xpath('.//*[@class="s-item__time-left"]/text()'):
				time_left = product.xpath('.//*[@class="s-item__time-left"]/text()').extract_first()
			else:
				time_left = 'No deadline'
			
			if product.xpath('.//*[@class="s-item__bids s-item__bidCount"]/text()'):
				bid_count = product.xpath('.//*[@class="s-item__bids s-item__bidCount"]/text()').extract_first()
			else: bid_count = 'No bids listed'

			yield{
			"Name":name,
			"Status":status,
			"Price":price,
			"Shipping Cost":shipping,
			"Time Remaining":time_left,
			"Current Bid Count": bid_count,
			"Link":link
			}
				
		# Get the next page
		next_page_url = response.xpath('//*/a[@class="x-pagination__control"][2]/@href').extract_first()

		# The last page do not have a valid url and ends with '#'
		if next_page_url == None or str(next_page_url).endswith("#"):
			self.log("eBay products collected successfully !!!")
		else:	
			print('\n'+'-'*30)		
			print('Next page: {}'.format(next_page_url))		
			yield scrapy.Request(next_page_url, callback=self.parse_link)       				


