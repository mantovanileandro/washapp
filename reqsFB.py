class reqsFB:
	def __init__(self,req):
		self.req = req

	def idSender(self):
		res = self.req['entry'][0]['messaging']
		for req in res:
			return req['sender']['id']
