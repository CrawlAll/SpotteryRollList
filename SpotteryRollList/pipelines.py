# -*- coding: utf-8 -*-
import pymysql
from scrapy.conf import settings
import pymongo


class SpotteryrolllistMongodbPipeline(object):
	def __init__(self, host, dbname, port, sheetname):
		self.host = host
		self.dbname = dbname
		self.port = port
		self.sheetname = sheetname

	@classmethod
	def from_crawler(cls, crawler):
		return cls(
			host=crawler.settings.get('MONGODB_HOST'),
			port=crawler.settings.get('MONGODB_PORT'),
			dbname=crawler.settings.get('MONGODB_DBNAME'),
			sheetname=crawler.settings.get('MONGODB_SHEETNAME')
		)

	def open_spider(self, spider):
		# 连接MONGODB
		self.client = pymongo.MongoClient(host=self.host, port=self.port)
		# 指定数据库
		self.mydb = self.client[self.dbname]
		# 存放数据的数据库表名
		self.sheet = self.mydb[self.sheetname]

	def process_item(self, item, spider):
		data = dict(item)
		self.sheet.insert(data)
		return item


class SpotteryrolllistMysqlPipeline(object):
	def __init__(self, host, dbname, user, pwd, port):
		self.host = host
		self.dbname = dbname
		self.user = user
		self.pwd = pwd
		self.port = port

	@classmethod
	def from_crawler(cls, crawler):
		return cls(
			host=crawler.settings.get('MYSQL_HOST'),
			dbname=crawler.settings.get('MYSQL_DBNAME'),
			user=crawler.settings.get('MYSQL_USER'),
			pwd=crawler.settings.get('MYSQL_PASSWD'),
			port=crawler.settings.get('MYSQL_PORT')
		)

	def open_spider(self, spider):
		self.connect = pymysql.connect(host=self.host, db=self.dbname, user=self.user, passwd=self.pwd, port=self.port,
									   charset='utf8', use_unicode=True)
		# 通过cursor执行增删查改
		self.cursor = self.connect.cursor()

	def process_item(self, item, spider):
		try:
			# 插入数据
			self.cursor.execute(
				"""insert into traditional_sporttery(series, pool, match_num, competing_team ,win_proportion, draw_proportion, lose_proportion, result, source)
value (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
				(item['series'], item['pool'], item['match_num'], item['competing_team'], item['win_proportion'],
				 item['draw_proportion'], item['lose_proportion'], item['result'], item['source']))
			self.connect.commit()

		except Exception as error:
			spider.logger.error(error)
		return item

	def close_spider(self, spider):
		self.connect.close()
