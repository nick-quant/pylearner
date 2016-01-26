from parsing_funcs import ParseQuestions
from parsing_funcs import ParseStatistics
from parsing_funcs import SaveStatistics
from subprocess import call
from question_queue import QuestionQueue
from datetime import timedelta
from datetime import datetime
import sys


def EvalAnswer(score_num):
	score = -1
	while score < 0 or score >= score_num:
		res = raw_input('Evaluate your answer: ')
		int_res = ""
		try:
			int_res = int(res)
			score = int_res
		except:
			print('Incorrect input')
			print('The evaluation should be between 0 and {}'.format(score_num))
	return score
	
def sys_args_to_dct():
	ret_dct = {}
	argc = len(sys.argv)
	for i in range(1, argc):
		arg = sys.argv[i]
		comps = arg.split('=')
		if len(comps) == 2 and comps[0].startswith('-'):		
			ret_dct[comps[0][1:]] = comps[1]
	return ret_dct

alpha = 1.0
beta = 7.0
min_delay = 60.0
chunk_size = 5
learn_tolerance = 2.0
scores = [-2, -0.5, 0.25, 1]
correct_answers = 5
learn_tolerance
min_height = correct_answers * max(scores)


#question_file = 'qbase.txt'
#stat_file = 'qstat.txt'
#question_file = 'patterns_base.txt'
#question_file = 'can_base.txt'
question_file = 'scvis_base.txt'
print("Command line arguments: ")
arg_dct = sys_args_to_dct()
print(arg_dct)
if "base" in arg_dct:
	question_file = arg_dct["base"]
	
stat_file =  'stat_' + question_file

questions, question_lst = ParseQuestions(question_file)

#for qid, q in questions.items():
#	q.console()
#	print('')
	
stat = ParseStatistics(stat_file, questions)
#for qid, lst in stat.items():
#	print(qid)
#	print(lst)

qq = QuestionQueue(question_lst, stat, scores, alpha, beta, chunk_size, min_height, timedelta(seconds = min_delay), learn_tolerance)
	
call(['cp', stat_file, 'tmp_{0}'.format(stat_file)])

command = 'd Eetjw*n4GJ20 P 5ERFD, pf'
call(['clear'])
test_q = qq.Next()
print(test_q.question)
while command != '@exit' and command != '@e':
	if command == '@save':
		print('Saving statistics')
		SaveStatistics(stat_file, stat)
	elif command == '@stat':
		print('Printing statistics')
	elif command == '@next' or command == '@n':
		call(['clear'])
		test_q = qq.Next()
		print(test_q.question)
	elif command == '@show' or command == '@s':
		print(test_q.answer)
		res = EvalAnswer(len(scores))
		if not test_q.qid in stat:
			stat[test_q.qid] = []
		stat[test_q.qid].append((datetime.now(), int(res)))
		SaveStatistics(stat_file, stat)
	command = raw_input(': ')
SaveStatistics(stat_file, stat)
