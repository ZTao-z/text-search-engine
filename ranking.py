import math
import numpy as np

class Ranking:
	def __init__(self, N):
		self.documentCount = N
		
	def IDF(self, word, dictionary):
		if word not in dictionary:
			return 0
		return math.log(self.documentCount / len(dictionary[word]))
		
	def TF(self, word, dictionary):
		rec = [0] * self.documentCount
		if word in dictionary:
			for f in dictionary[word]:
				info = f.split("-")
				index = int(info[0].split(".")[0])
				frequency = int(info[1])
				rec[index-1] = math.log(1+frequency)
		return rec
		
	def TF_idf(self, word, dictionary):
		idf = self.IDF(word, dictionary)
		tf = self.TF(word, dictionary)
		t = np.array(tf)
		w = t * idf
		return w
		
	def run(self, query, dictionary):
		res = np.array([0.0] * self.documentCount)
		for word in query:
			w = self.TF_idf(word, dictionary)
			res += w
		return res