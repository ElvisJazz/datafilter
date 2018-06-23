# -*- conding: utf-8 -*-
# @Time    : 2018/6/21 15:45
# @Author  : Elvis Jia
# @Description: parser test


from config import ConfigParser
import requests

if __name__ == "__main__":
	configParser = ConfigParser('config.txt')
	rootBlock = configParser.parse()

	# Test read html file
	with open('test.htm', 'rb') as reader:
		content = reader.read().decode('utf-8')
		result, stop = rootBlock.search(content, 0, len(content))
		print 'test html:', result

	# Test download html
	url = 'https://mall.kaola.com/search.html?shopId=15662189'
	content = requests.get(url, verify=False).text
	result, stop = rootBlock.search(content, 0, len(content))
	print 'test html downloaded:', result