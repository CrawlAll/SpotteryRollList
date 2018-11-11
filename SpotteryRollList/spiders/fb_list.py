# -*- coding: utf-8 -*-
import re
import scrapy
from lxml import etree
from SpotteryRollList.items import SpotteryrolllistItem


class FbListSpider(scrapy.Spider):
	name = 'fb_list'
	allowed_domains = ['sporttery.cn']

	url = r'http://info.sporttery.cn/roll/fb_list.php?page='
	offset = 1
	start_urls = [url + str(offset) + '&c=%D7%E3%B2%CA%CA%A4%B8%BA']

	def parse(self, response):
		# 从第一页提取出来总页数，并设置为全局变量，便于最后判断
		if response.url == self.start_urls[0]:
			page_url = response.xpath("//table[@class='m-page']//ul/li[@class='u-pg1'][2]/a/@href").extract()[0]
			page = int(re.findall(r'\d{3}', page_url)[0])
			global page

		# 第一层下的url及标题名字
		url_list = response.xpath('//ul/li/span/a/@href').extract()
		title_list = response.xpath('//ul/li/span/a/text()').extract()

		for i in range(len(url_list)):
			item = SpotteryrolllistItem()
			detail_url = url_list[i]
			detail_title = title_list[i]
			if '冷门' in detail_title:
				# 0代表--14场，1代表--任9
				if '期冷门' in detail_title:
					item['pool'] = 0
					item['series'] = re.findall(r'\d{5}', detail_title)[0]
					yield scrapy.Request(url=detail_url, meta={'meta_1': item}, callback=self.second_parse)
				elif '期任九冷门' in detail_title or '期任9冷门' in detail_title:
					item['pool'] = 1
					item['series'] = re.findall(r'\d{5}', detail_title)[0]
					yield scrapy.Request(url=detail_url, meta={'meta_1': item}, callback=self.second_parse)
				else:
					self.logger.info(detail_title + detail_url)

	def second_parse(self, response):
		meta_1 = response.meta['meta_1']
		item = SpotteryrolllistItem()
		item['pool'] = meta_1['pool']
		item['series'] = meta_1['series']
		item['source'] = response.url

		tr_list = response.xpath('//table/tbody/tr')
		for td_list in tr_list:
			# 判断该tr行中的每个td下是否存在'VS'，列表为空说明不符合数据提取要求，跳过
			if len(re.findall(r'VS', td_list.extract())):
				tree = etree.HTML(td_list.extract())
				match_num = tree.xpath('//td[2]')[0].xpath('string(.)')
				item['match_num'] = match_num
				competing_team = tree.xpath('//td[3]')[0].xpath('string(.)')
				item['competing_team'] = competing_team
				win_proportion = tree.xpath('//td[4]')[0].xpath('string(.)')
				item['win_proportion'] = win_proportion
				draw_proportion = tree.xpath('//td[5]')[0].xpath('string(.)')
				item['draw_proportion'] = draw_proportion
				lose_proportion = tree.xpath('//td[6]')[0].xpath('string(.)')
				item['lose_proportion'] = lose_proportion
				result = tree.xpath('//td[7]')[0].xpath('string(.)')
				item['result'] = result
				yield item

		if self.offset <= page:
			self.offset += 1
		# 发送下一页请求
		yield scrapy.Request(self.url + str(self.offset) + '&c=%D7%E3%B2%CA%CA%A4%B8%BA', callback=self.parse)
