import os
import json
import requests
import urllib2
from reqsFB import reqsFB
from reqsbackend import reqsbackend



class menusFB:
	def __init__(self,url,token,req):
		self.url = url + token
		self.clienteFB = reqsFB(req)
		self.req = req
		self.reqbackend = reqsbackend()
		self.token = token
		
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
		print res


	def mostrarLaundrys(self,laundrys):
		payload = {}
		payload['recipient'] = {"id":self.clienteFB.idSender()}
		payload['message'] = {"attachment":{}}
		payload['message']['attachment']['type'] = 'template'
		payload['message']['attachment']['payload'] = {}
		payload['message']['attachment']['payload']['template_type'] = 'generic'
		payload['message']['attachment']['payload']['elements'] = []
		button = {"type":"postback","title":"Volver","payload":"SELECT_LAUNDRY_VOLVER"}

		for laundry in laundrys:
			btns = []
			btns.append(button)
			
			postback = 'SELECT_LAUNDRY_ID_%s' %laundry['id']
			button = {"type":"postback","title":"Seleccionar","payload": postback}

			desc = json.loads(laundry['desc'])
			element = {desc, "buttons" : btns}
			payload['message']['attachment']['payload']['elements'].append(element)
			
			#element = {"title": "rift","subtitle": "Next-generation virtual reality","image_url": "http://messengerdemo.parseapp.com/img/rift.png"}
			#payload['message']['attachment']['payload']['elements'].append(element)


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







