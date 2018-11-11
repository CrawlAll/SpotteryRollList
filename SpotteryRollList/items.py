# -*- coding: utf-8 -*-
import scrapy


class SpotteryrolllistItem(scrapy.Item):
	# 1、第几期
	series = scrapy.Field()
	# 2、奖池类型(玩法)
	pool = scrapy.Field()
	# 3、场号：
	match_num = scrapy.Field()
	# 4、主客队名：
	competing_team = scrapy.Field()
	# 5、猜胜比例：
	win_proportion = scrapy.Field()
	# 6、猜平比例：
	draw_proportion = scrapy.Field()
	# 7、猜负比例：
	lose_proportion = scrapy.Field()
	# 8、实际比赛结果：
	result = scrapy.Field()
	# 9、该数据来源的url
	source = scrapy.Field()
