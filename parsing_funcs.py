from datetime import datetime
from test_question import TestQuestion
from test_question import TestQuestionBuilder

def ParseQuestions(file_name):
	questions = {}
	questions_lst = []
	parse = -1
	with open(file_name, 'r') as f:
		qb = TestQuestionBuilder()
		for line in f:
			if line.startswith('###id:'):
				qb.Clear()
				qb.qid = line.split(':')[1].rstrip()
			elif line.startswith('###end'):
				q = qb.Build()
				if q != None:
					questions[q.qid] = q
					questions_lst.append(q)
				parse = -1
			elif line.startswith('###q:'):
				parse = 0
			elif line.startswith('###a:'):
				parse = 1
			elif parse == 0:
				qb.question += line
			elif parse == 1:
				qb.answer += line
		q = qb.Build()
		if q != None:
			questions[q.qid] = q
			questions_lst.append(q)
	return questions, questions_lst

def ParseStatistics(file_name, questions):
	statistics = {}
	with open(file_name, 'r') as f:
		cur_id = -1
		for line in f:
			if line.startswith('###id:'):
				tmp_id = line.split(':')[1].rstrip()			
				if tmp_id in questions:
					cur_id = tmp_id
					statistics[cur_id] = []
			else:
				try:					
					dt_arr = line.split('&')					
					dt_str = dt_arr[0].strip()
					res = int(dt_arr[1].strip())									
					dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S.%f')
					statistics[cur_id].append((dt, res))
				except:
					a = 2
	return statistics

def SaveStatistics(file_name, statistics):
	with open(file_name, 'w') as f:
		for qid, lst in statistics.items():
			f.write('###id:{0}\n'.format(qid))
			for dt, res in lst:
				f.write('{0} & {1}\n'.format(dt, res))
