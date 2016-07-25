import requests

class reqsbackend:
	def __init__(self):
		self.url = "http://172.31.15.182/"

	def estaCompleto(self,idfb):
		datos = []
		res = requests.get(self.url + "user/fb/" + idfb + "/detail")
		res = res.json()
		for key in res:
			if res[key] == None:
				datos.append(key)
		return datos


	def existeUser(self,idfb):
		res = requests.get(self.url + '/fb/' + idfb).json()
		return res['exist']


	def crearUser(self,payload):
		user_datos = payload

		res = requests.post(self.url + 'insert', payload=user_datos)
		if res['response'] is 'successful':
			return True
		else:
			return False
