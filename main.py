# encoding=utf-8

from index import *
from ranking import *
from search import *
import json, os
from queue import PriorityQueue

root = './data/page/'

def getFileList():
	fileList = [x for x in os.listdir(root) if os.path.isfile(root+x) and os.path.splitext(x)[1]=='.txt']
	return fileList

if __name__ == "__main__":
	files = getFileList()
	l = []
	for file in files:
		with open(root+file, "r", encoding="utf8") as f:
			content= []
			for line in f.readlines():
				content.append(line)
			l.append([file] + [content])
	
	ii = InvertedIndexing()
	rank = Ranking(len(files))
	search = Search()
	dictionary = {}
	
	for line in l:
		ii.run(line[0], "".join(line[1]), dictionary)
	
	while(True):
		query = search.run(dictionary)
		print("搜索关键字：", query)
		if query[0] == "0":
			break
		docRank = rank.run(query, dictionary)
		docList = PriorityQueue()
		count = 1
		for i in range(len(docRank)):
			if docRank[i] > 0:
				docList.put((docRank[i] * -1, "%d.txt" % (i+1)))
				count += 1
		print("共有%d个结果，优先级从大到小排列如下：" % (count-1))
		count = 1
		while not docList.empty():
			print("%03d.\t%s" % (count, docList.get()[1]))
			count += 1
		print("-----------------------------------------------")