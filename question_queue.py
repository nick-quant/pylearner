from math import pow
from math import ceil
from datetime import datetime
from time import sleep

class QuestionQueue:
	def __init__(self, q_lst, stat, scores, alpha, beta, chunk_size, min_height, min_delay, learn_tolerance = 0):
		# min height of the triangle
		self.scores = scores
		#self.alpha = alpha
		self.alpha = pow(min_height, 1 - beta)
		self.beta = beta
		self.chunk_size = chunk_size
		self.min_height = min_height
		self.q_lst = q_lst
		self.stat = stat
		self.min_delay = min_delay
		self.learn_tolerance = learn_tolerance
		first_score = 0
		if self.q_lst[0].qid in self.stat:
			first_score = self._CalcTotalScore(self.q_lst[0].qid)
		self._m = max(self.min_height, first_score)
		self.N = self.chunk_size
		self._MaximizeTriangle()


	def _FillTriangleList(self):	
		self._triangle_lst = list([ceil(max(self._m * (1 - float(i) / self.N), 0)) for i in range(len(self.q_lst))])
		print('triangle list: {}'.format(self._triangle_lst))
	
	def _CalcTotalScore(self, qid):
		ssum = 0
		if not qid in self.stat:
			return 0
		for dt, res in self.stat[qid]:
			ssum += self.scores[res]
		return ssum
		
	def _TriangleFilled(self):
		id_lst = list([i for i in range(min(self.N, len(self.q_lst)))])
		# after filtering only the items remain where we are less than triangle
		not_learned = list(filter(lambda i: self._triangle_lst[i] > self._CalcTotalScore(self.q_lst[i].qid), id_lst))
		print('Not learned: {}'.format(not_learned))
		if len(not_learned) <= self.learn_tolerance:
			return True
		else:
			return False
	
	def _MaximizeTriangle(self):
		print('N:{}\t, m:{}'.format(self.N, self._m))
		self._FillTriangleList()
		while self._TriangleFilled():
			print('Triangle filled')
			self.N += self.chunk_size
			self._m = pow(self.N / self.alpha, 1 / self.beta)
			print('N:{}\t, m:{}'.format(self.N, self._m))
			# We changed the two coefficients of the triangle equation. We are ready to recalculate the triangle
			self._FillTriangleList()
		
	def Next(self):
		# Now we are ready to check whether the triangle is filled. If yes we would like to change the triangle
		self._MaximizeTriangle()
		# upside is the list of the the differences of what we have and what should have 
		upside = list([self._CalcTotalScore(self.q_lst[i].qid) - self._triangle_lst[i] for i in range( min(self.N, len(self.q_lst)) )])
		print('upside: {}'.format(upside))
		print('upside sum: {}'.format(sum(upside)))
		upside_sorted_id = list([i[0] for i in sorted(enumerate(upside), key=lambda x:x[1])])
		print('upside_sorted_id: {}'.format(upside_sorted_id))
		# So now we have the questions with higher priority first, but we have to chek whether they have been called lately,
		# because then we may skip them
		last_allowed_time = datetime.now() - self.min_delay
		print('last time: {}'.format(last_allowed_time))
		for i in range(min(self.N, len(self.q_lst))):
			q = self.q_lst[upside_sorted_id[i]]
			qid = q.qid
			print(qid)
			if qid in self.stat: # if we have some entry for this qid, we better check if it is of lately time
				print(self.stat[qid][-1][0])
				print(last_allowed_time)
				if self.stat[qid][-1][0] <= last_allowed_time:															
					return q
			else: # No stats, no reason to skip the question
				return q
		sleep(1)
		return self.Next()
		
		
