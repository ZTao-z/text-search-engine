# encoding=utf-8
import nltk, jieba
import re, string
from jieba import posseg

class Search:
	stopwords = ["的", "是"]
	
	def __init__(self):
		pass
		
	def getInput(self):
		queryStr = input('请输入搜索内容：')
		rmSymbol_Lines = self.preprocess(queryStr)
		wordList = []
		for line in rmSymbol_Lines:
			wordList = wordList + self.cutWords(line.strip())
		return wordList
	
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
		
	def editdis_dp(self, str1, str2):
		len_str1 = len(str1)+1
		len_str2 = len(str2)+1
		dp = [[0 for i in range(len_str2)] for n in range(len_str1)]
		for i in range(len_str2):
			dp[0][i] = i
		for i in range(len_str1):
			dp[i][0] = i
		for i in range(1, len_str1):
			for j in range(1, len_str2):
				if str1[i-1] == str2[j-1]:
					dp[i][j] = dp[i-1][j-1]
				else:
					dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])+1
		return dp[len_str1-1][len_str2-1]

	def run(self, dictionary):
		queryCut = self.getInput()
		queryArr = []
		for word in queryCut:
			if word not in dictionary:
				print("没有找到",word,"相关结果，展示近似结果....")
				min_distance = 1000000
				min_dis_word = ""
				for rep in list(dictionary.keys()):
					min_d = self.editdis_dp(word, rep)
					if min_d < min_distance:
						min_distance = min_d
						min_dis_word = rep
				queryArr.append(min_dis_word)
			else:
				queryArr.append(word)
		return queryArr