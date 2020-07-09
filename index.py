# encoding=utf-8
import nltk, jieba
import re, string
from jieba import posseg

class InvertedIndexing:
	stopwords = ["的", "是"]
	
	def __init__(self):
		pass
		
	def preprocess(self, line):
		res = []
		illegal_char = string.punctuation + '【·！…（）—：“”？《》、；，。】' 
		pattern = re.compile('[%s]' % re.escape(illegal_char))
		res = [m for m in pattern.split(line) if m != '']
		return res
	
	def cutWords(self, line):
		split_word = jieba.cut(line,cut_all=False)
		result = []
		for singleWord in split_word:
			if singleWord not in self.stopwords:
				result.append(singleWord)
		return result
		
	def buildUpIndex(self, wordList):
		obj = dict()
		for index in range(len(wordList)):
			if wordList[index] in obj:
				obj[wordList[index]].append(str(index))
			else:
				obj[wordList[index]] = [str(index)]
		return obj
		
	def run(self, filename, data, total_dictionary):
		# data为文本数据(单个文件)
		rmSymbol_Lines = self.preprocess(data)
		# 切割单词
		wordList = []
		for line in rmSymbol_Lines:
			wordList = wordList + self.cutWords(line.strip())
		index_dict = self.buildUpIndex(wordList)
		for key, value in index_dict.items():
			if key in total_dictionary:
				total_dictionary[key].append("%s-%d-%s" % (filename, len(value), ",".join(value)))
			else:
				s = "%s-%d-%s" % (filename, len(value), ",".join(value))
				total_dictionary[key] = [s]
		return total_dictionary