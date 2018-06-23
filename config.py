# -*- conding: utf-8 -*-
# @Time    : 2018/6/21 15:45
# @Author  : Elvis Jia
# @Description: Config


from block import SearchTargetBlock, SearchBoundBlock
import json
import re


class ConfigParser(object):

	def __init__(self, path):
		with open(path, 'r') as reader:
			newLines = [re.sub(r'//.*', '', line, 0) for line in reader.readlines()]
			content = ''.join(newLines)
			print content
			self.content = json.loads(content)
		self._parseMethod = {
			'BB': self._parseAsBoundBlock,
			'TB': self._parseAsTargetBlock,
		}

	def parse(self):
		element = self.content
		return self._parse(element)

	def _parse(self, e):
		method = self._parseMethod.get(e[0])
		if not method:
			raise RuntimeError('No method for parsing, check config!')
		return method(e[1:])

	def _parseAsBoundBlock(self, e):
		block = SearchBoundBlock(*e[:7])
		if len(e) > 7:
			for ie in e[7:]:
				block.addChild(self._parse(ie))
		return block

	def _parseAsTargetBlock(self, e):
		block = SearchTargetBlock(*e[:7])
		return block

