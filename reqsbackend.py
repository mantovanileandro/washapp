import requests
import json


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

		res = requests.post(self.url + 'user/insert', data=json.dumps(user_datos))
		if res['response'] is 'successful':
			return True
		else:
			return False


	def getUserLocation(self,fbid):
		res = requests.get(self.url + "user/fb/" + fbid + "/detail").json()
		return res['localidad']


	def getLastPedido(self,fbid):
		#obtener el ultimo pedido COMPLETADO (hay que cambiar la api de backend)
		payload = {}
		payload['user_id'] = fbid
		res = requests.post(self.url + 'pedido/detail',data=json.dumps(payload)).json()

		if not ('error' in res['response']):
			return res['response']
		else:
			return None


	def setNewPedido(self,fbid,laundry_id):

			payload = {}
			payload['user_fb'] = fbid
			payload['laundry'] = laundry_id
			payload['status'] = 'new'

			res = requests.post(self.url + 'pedido/new', data = json.dumps(payload)).json()

			print res

			if res['response'] is 'successful':
				return True
			else:
				return False


	def getAllLaundrys(self,localidad):
		payload = {}
		payload['localidad'] = localidad
		res = requests.post(self.url + 'laundry/getall',data=json.dumps(payload)).json()

		if not ('error' in res['response']):
			return res
		else:
			return None







