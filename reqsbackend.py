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
		res = requests.get(self.url + 'user/fb/' + idfb).json()
		return res['exist']


	def crearUser(self,payload):
		user_datos = payload

		res = requests.post(self.url + 'user/insert', data=user_datos)
		if res['response'] is 'successful':
			return True
		else:
			return False


	def getLastPedido(self,fbid):
		#obtener el ultimo pedido COMPLETADO (hay que cambiar la api de backend)
		payload = {'user_id': fbid}
		res = requests.post(self.url + 'user/detail',data=payload).json()

		print res

		if not ('error' in res['response']):
			return res['response']
		else:
			return None
