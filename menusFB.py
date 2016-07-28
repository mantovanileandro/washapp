import os
import json
import requests
import urllib2
from reqsFB import reqsFB
from reqsbackend import reqsbackend



class menusFB:
	def __init__(self,url,token,req,usuarios_faltantes):
		self.url = url + token
		self.clienteFB = reqsFB(req)
		self.req = req
		self.reqbackend = reqsbackend()
		self.token = token
		self.preguntas = {"localidad" : "De que localidad sos?" , "address" : "Como es tu direccion?"}
		self.usuarios_faltantes = usuarios_faltantes
	def mostrarRepetirPedido(self):
		payload = {}
		payload['recipient'] = {"id": self.clienteFB.idSender()}
		payload['message'] = {}
		payload['message']['text'] = 'Te gustaria repetir el pedido anterior ? :)'


		quick_replie = {}
		quick_replie['content_type'] = 'text'
		quick_replie['title'] = 'Si'
		quick_replie['payload'] = 'PEDIDO_REPETIR_QUICK_REPLIE_YES'

		quick_replie_2 = {}
		quick_replie_2['content_type'] = 'text'
		quick_replie_2['title'] = 'No'
		quick_replie_2['payload'] = 'PEDIDO_REPETIR_QUICK_REPLIE_NO'

		quick_replie_3 = {}
		quick_replie_3['content_type'] = 'text'
		quick_replie_3['title'] = 'Cambiar Lavanderia'
		quick_replie_3['payload'] = 'PEDIDO_REPETIR_QUICK_REPLIE_CAMBIAR_LAUNDRY'

		quick_replie_4 = {}
		quick_replie_4['content_type'] = 'text'
		quick_replie_4['title'] = 'Cambiar Horario'
		quick_replie_4['payload'] = 'PEDIDO_REPETIR_QUICK_REPLIE_CAMBIAR_HORARIO'


		payload['message']['quick_replies'] = [quick_replie, quick_replie_2, quick_replie_3, quick_replie_4]

		print quick_replie_3['payload']
		res = requests.post(self.url, json=payload)


	def menu_principal(self):
		payload = {}
		payload['recipient'] = {"id": self.clienteFB.idSender()}
		payload['message'] = {"attachment":{}}
		payload['message']['attachment']['type'] = 'template'
		payload['message']['attachment']['payload'] = {}
		payload['message']['attachment']['payload']['template_type'] = 'button'
		payload['message']['attachment']['payload']['text'] = 'Principal Menu'
		payload['message']['attachment']['payload']['buttons'] = []

		button = {"type":"postback","title":"Tutorial","payload":"PRINCIPAL_TUTORIAL"}
		payload['message']['attachment']['payload']['buttons'].append(button)
		button = {"type":"postback","title":"Nuevo Pedido","payload":"PRINCIPAL_PEDIDO"}
		payload['message']['attachment']['payload']['buttons'].append(button)
		button = {"type":"postback","title":"Status","payload":"PRINCIPAL_STATUS"}
		payload['message']['attachment']['payload']['buttons'].append(button)

		res = requests.post(self.url,json=payload)

	def mostrarTutorial(self):
		payload = {}
		payload['recipient'] = {"id":self.clienteFB.idSender()}
		payload['message'] = {"attachment":{}}
		payload['message']['attachment']['type'] = 'template'
		payload['message']['attachment']['payload'] = {}
		payload['message']['attachment']['payload']['template_type'] = 'generic'
		payload['message']['attachment']['payload']['elements'] = []
		button = {"type":"postback","title":"Volver","payload":"TUTORIAL_VOLVER"}
		element = {"title": "rift","subtitle": "Next-generation virtual reality","image_url": "http://messengerdemo.parseapp.com/img/rift.png","buttons" : [button]}
		payload['message']['attachment']['payload']['elements'].append(element)
		element = {"title": "rift","subtitle": "Next-generation virtual reality","image_url": "http://messengerdemo.parseapp.com/img/rift.png"}
		payload['message']['attachment']['payload']['elements'].append(element)


		res = requests.post(self.url,json=payload)


	def mostrarLaundrys(self,laundrys,scope):
		payload = {}
		payload['recipient'] = {"id":self.clienteFB.idSender()}
		payload['message'] = {"attachment":{}}
		payload['message']['attachment']['type'] = 'template'
		payload['message']['attachment']['payload'] = {}
		payload['message']['attachment']['payload']['template_type'] = 'generic'
		payload['message']['attachment']['payload']['elements'] = []
		button = {"type":"postback","title":"Volver","payload":"SELECT_LAUNDRY_VOLVER"}


		for laundry in laundrys['laundrys']:

			btns = []
			
			postback = 'SELECT_LAUNDRY_%s_ID_%s' %(scope, laundry['id'])
			button2 = {"type":"postback","title":"Seleccionar","payload": postback}
			btns.append(button2)

			btns.append(button)

			element = json.loads(laundry['desc'])
			element["buttons"] = btns
			payload['message']['attachment']['payload']['elements'].append(element)


		res = requests.post(self.url,json=payload)


	def enviarMensaje(self,texto):
		payload = {"recipient": {"id":self.clienteFB.idSender()},"message": {"text":texto}}
		res = requests.post(self.url,json=payload)

	def contieneTexto(self,texto):
		res = self.req['entry'][0]['messaging']

		for req in res:
			if req.has_key('message'):
				if req['message'].has_key('text'):
					if req['message']['text'].lower() == texto:
						return True
		return False

	def get_texto(self):
		res = self.req['entry'][0]['messaging'][0]['message']['text']
		print "TEXTO   " + res
		return res		

	def guardar_y_solicitar_dato(self):
		if self.usuarios_faltantes.has_key(self.clienteFB.idSender()):
			self.reqbackend.modify(self.usuarios_faltantes[self.clienteFB.idSender()],self.get_texto(),self.clienteFB.idSender())
			if self.reqbackend.estaCompleto(self.clienteFB.idSender()):
				return False
			else:
				return True


	def pedirDato(self):
		datos = self.reqbackend.estaCompleto(self.clienteFB.idSender())
		self.enviarMensaje(self.preguntas[datos[0]])
		self.usuarios_faltantes[self.clienteFB.idSender()] = datos[0]
