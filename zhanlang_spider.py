# -*- coding:utf-8 -*-
""" 抓取豆瓣电影的战狼影评
手动装载的登录后的关键cookies
"""
import os
import sys
import requests
import random
import logging
import logging.config
from time import sleep
from lxml import etree

reload(sys)
sys.setdefaultencoding('utf-8')


# 配置日志文件
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "basic": {
            "format": "%(levelname)s - %(asctime)s - %(module)s - %(message)s"
        }
    },
    "handlers": {
        "info_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "basic",
            "filename": os.path.join(BASE_DIR, "zhanlang.log"),
            "encoding": "utf8"
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["info_file_handler"]
    }
}
logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)

# 配置请求头信息
USER_AGENTS = [
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_0) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4",
	"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_0; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.206.1 Safari/532.0",
	"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_0; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.204.0 Safari/532.0",
	"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_0; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.203.4 Safari/532.0",
	"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_0; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.203.0 Safari/532.0",
	"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_0; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.202.0 Safari/532.0",
	"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_0; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.212.1 Safari/532.1",
	"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_0; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.375.99 Safari/533.4",
	"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_0; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.375.86 Safari/533.4",
	"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_0; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.307.11 Safari/532.9",
	"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_0; en-US) AppleWebKit/528.10 (KHTML, like Gecko) Chrome/2.0.157.2 Safari/528.10",
	"Mozilla/5.0 (Macintosh; U; Mac OS X 10_6_1; en-US) AppleWebKit/530.5 (KHTML, like Gecko) Chrome/ Safari/530.5",
	"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.222.4 Safari/532.2"
]

HEADER = {
    'User-Agent': random.choice(USER_AGENTS),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate',
}
	

def main():
	session =requests.session()
	cookies = {"dbcl2": "120962264:pwtS4X8yrCg"}
	for index in xrange(7000, 10000, 20):
		# 爬取战狼评论
		logger.info(u'爬取战狼第{}条评论'.format(index))
		try:
			response = session.get('https://movie.douban.com/subject/26363254/comments?start={}&limit=20&sort=new_score&status=P'.format(index), cookies=cookies)
			if response.status_code != 200:
				logger.error('failed, response status is {} not 200'.format(response.status_code))
				break
			else:
				logger.info('success.')
		except Exception as e:
			logger.exception(e)
		
		# 解析评论
		selector = etree.HTML(response.content)
		items = selector.xpath("//*[@id='comments']/div")
		comments = []
		for item in items:
			try:
				comment = item.xpath(".//*[@class='comment']/p/text()")[0].strip()
				comments.append(comment)
			except IndexError:
				pass

		# 保存到文件
		file_path = os.path.join(BASE_DIR, "zhanlang_comments")
		with open(file_path, 'a') as f:
			for comment in comments:
				f.write('{}\n'.format(comment))
		sleep(5)


if __name__ == '__main__':
	main()
