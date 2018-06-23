# -*- coding: utf-8 -*-
# @Time    : 2018/6/21 15:45
# @Author  : Elvis Jia
# @Description: Block for search


class SearchBoundBlockType:
	ORDERED_SEARCH = 1
	SURROUNDED_SEARCH = 2


class Block(object):

	def __init__(self, tag1, tag2, offset1=None, offset2=None):
		self.tag1 = tag1
		self.tag2 = tag2
		self.offset1 = offset1 if offset1 is not None else len(tag1)
		self.offset2 = offset2 if offset2 is not None else 0

	def search(self, content, startIdx, endIdx):
		raise NotImplementedError


class SearchTargetBlock(Block):

	def __init__(self, title, failStop, tag2First, tag1, offset1, tag2, offset2):
		super(SearchTargetBlock, self).__init__(tag1, tag2, offset1, offset2)
		self.title = title
		self.failStop = failStop
		self.tag2First = tag2First

	def search(self, content, startIdx, endIdx):
		if self.tag2First:
			idx2 = content.find(self.tag2, startIdx, endIdx) + self.offset2
			idx1 = content.rfind(self.tag1, startIdx, idx2) + self.offset1
		else:
			idx1 = content.find(self.tag1, startIdx, endIdx) + self.offset1
			idx2 = content.find(self.tag2, idx1, endIdx) + self.offset2
		if idx1 < 0 or idx2 < 0:
			res = None
		else:
			res = {self.title: content[idx1: idx2].strip()}
		return res, self.failStop and not res


class SearchBoundBlock(Block):

	SearchMethod = {
		SearchBoundBlockType.ORDERED_SEARCH: 'searchInOrder',
		SearchBoundBlockType.SURROUNDED_SEARCH: 'searchWithSurround',
	}

	def __init__(self, searchType, searchCnt, searchChildSucCnt, tag1, offset1, tag2, offset2):
		assert searchCnt != 0 , 'searchCnt should not be 0!'
		super(SearchBoundBlock, self).__init__(tag1, tag2, offset1, offset2)
		self.searchType = searchType
		self.searchCnt = searchCnt
		self.searchChildSucCnt = searchChildSucCnt
		self.children = []

	def addChild(self, child):
		self.children.append(child)

	def search(self, content, startIdx, endIdx):
		method = getattr(self, self.SearchMethod.get(self.searchType))
		if method:
			cnt = 0
			results = []
			while self.searchCnt < 0 or cnt < self.searchCnt:
				res, tag2Idx, stop = method(content, startIdx, endIdx)
				if not res:
					break
				results.extend(res)
				startIdx = tag2Idx + len(self.tag2)
				cnt += 1
				if stop:
					break
			return results, not results
		else:
			return None, True

	def searchInOrder(self, content, startIdx, endIdx):
		idx1 = content.find(self.tag1, startIdx, endIdx) + self.offset1
		idx2 = content.find(self.tag2, idx1, endIdx)
		if idx1 < 0 or idx2 < 0:
			return None, idx2, False
		idx1 += self.offset1
		idx2 += self.offset2
		results = self.searchInChildren(content, idx1, idx2)
		return results, idx2, False

	def searchWithSurround(self, content, startIdx, endIdx):
		idx1 = content.find(self.tag1, startIdx, endIdx)
		idx2 = content.find(self.tag2, idx1, endIdx)
		if idx1 < 0 or idx2 < 0:
			return None, idx2, False
		idx1 += self.offset1
		idx2 += self.offset2
		results = self.searchInChildren(content, idx1, idx2)
		return results, idx2, True

	def searchInChildren(self, content, startIdx, endIdx):
		tbResult = {}
		results = []
		for child in self.children:
			res, stop = child.search(content, startIdx, endIdx)
			if res:
				if isinstance(child, SearchBoundBlock):
					results.append(res)
				elif isinstance(child, SearchTargetBlock):
					tbResult.update(res)
				if self.searchChildSucCnt > 0 and len(tbResult)+len(results) >= self.searchChildSucCnt:
					break
			if stop:
				break
		if tbResult:
			results.append(tbResult)
		return results


