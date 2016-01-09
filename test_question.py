class TestQuestion:
	def __init__(self, qid, question, answer):
		self.qid = qid
		self.question = question
		self.answer= answer
	
	def console(self):
		print(self.qid)
		print(self.question)
		print(self.answer)

class TestQuestionBuilder:
	def __init__(self):
		self.qid = -1
		self.question = ''
		self.answer = ''
	
	def Build(self):
		if self.qid != -1:
			return TestQuestion(self.qid, self.question, self.answer)
		else:
			return None
				
	def Clear(self):
		self.qid = -1
		self.question = ''
		self.answer = ''


