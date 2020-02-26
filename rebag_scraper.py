# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from selenium import webdriver
from selenium.webdriver.common.by import By

class RebaggioSpider(scrapy.Spider):
    name = "rebaggio"
    allowed_domains = ["rebag.com"]
    start_urls = ["https://shop.rebag.com/collections/all-bags?_=pf&pf_v_designers=Christian+Louboutin&pf_st_availability_hidden=true"]
    
    def __init__(self):
        self.driver = webdriver.Chrome()

    def parse(self, response):
        self.driver.get(response.url)
        self.driver.implicitly_wait(4)
        bags = self.driver.find_elements(By.XPATH,'//div[@class="product-caption"]')
        for bag in bags:
            #vendor = bag.find_element(By.XPATH,'//div[@class="product-vendor"]')
            url = response.url
            title = bag.find_element(By.XPATH, './div[@class="product-caption-top"]/a[@class="product-title"]').text
            vendor = bag.find_element(By.XPATH, './div[@class="product-caption-top"]/a[@class="product-vendor"]').text
            price = bag.find_element(By.XPATH,'./div[@class="product-caption-bottom"]/a[@class="product-price"]/span[@class="bc-sf-filter-product-item-regular-price"]').text
            
            #yield Request(url, callback=self.parse_page, meta={'URL': url, 'Title': title, 'Vendor':vendor, 'Price': price})
            print(url)
            print(title)
            print(price)
            yield { "url": url, "vendor": vendor, "title": title, "price": price }
        
        url = self.driver.find_elements(By.XPATH,'//span[@class="next"]/a')
        if(len(url)):
            url = url[0].get_attribute("href")
            yield Request(url, callback=self.parse)
        else:
            url = None
        #print("URL", url)

        
    def parse_page(self, response):
        url = response.meta.get('URL')
        title = response.meta.get('Title')
        vendor = response.meta.get('Vendor')
        price = response.meta.get("Price")
       
        yield{'URL': url, 'Title': title, 'Vendor':vendor, "Price": price }

        
        #print(bags)


        #link = response.xpath('//div[@class="bc-sf-filter-bottom-pagination-default pagination"]')
        
       
        # name = response.xpath('//a[@class="product-title"]/text()').extract()
        # price = response.xpath('//a[@class="product-price"]/text()').extract()
        # condition = response.xpath('//a[@class="product-caption-bottom"]').extract()
        # relative_url = response.xpath('//a/@href').extract_first()
        # print(name)
        # print(price)
        # print(condition)
        # print(relative_url)

            #print(bag.extract())
        #     name = bag.xpath('.//[@class="product-title"]//text()').extract_first()
        #     price = bag.xpath('.//*[@class="bc-sf-filter-product-item-regular-price"]/text()').extract_first()
        #     condition = bag.xpath('.//*[@class="product-condition"]/text()').extract_first()
        #     relative_url = bag.xpath('a/@href').extract_first()
        # yield {
        #           "Name": name,
        #           "Status": condition,
        #           "Price": price,
        #           "Link": "https://shop.rebag.com/" + relative_url
        #     }