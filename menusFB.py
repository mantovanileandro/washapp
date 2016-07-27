import os
import json
import requests
import urllib2
from reqsFB import reqsFB
from reqsbackend import reqsbackend


def buscarUsuarioEnDic(dic,fbid):
        for id_fb in dic:
                if id_fb == fbid:
                        return True
        return False


class menusFB:
	def __init__(self,url,token,req):
		self.url = url + token
		self.clienteFB = reqsFB(req)
		self.req = req
		self.reqbackend = reqsbackend()
		self.token = token
		self.preguntas = {"INICIA" : "De que localidad sos?" , "LOCALIDAD" : "De que localidad sos?" , "DIRECCION" : "Como es tu direccion?"}

	def mostrarRepetirPedido(self):
		payload = {}
		payload['recipient'] = {"id": self.clienteFB.idSender()}
		payload['message'] = {}
		payload['message']['text'] = 'Te gustaria repetir el pedido anterior ? :)'
		

		quick_replie = {}
		quick_replie['content_type'] = 'text'
		quick_replie['title'] = 'Si :)'
		quick_replie['payload'] = 'PEDIDO_REPETIR_QUICK_REPLIE_YES'

		quick_replie_2 = {}
		quick_replie_2['content_type'] = 'text'
		quick_replie_2['title'] = 'No :('
		quick_replie_2['payload'] = 'PEDIDO_REPETIR_QUICK_REPLIE_NO'

		print payload['message']
		print payload['message']['quick_replies']

		payload['message']['quick_replies'] = [quick_replie, quick_replie_2]

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


		print "laundrys ----------"
		#print laundrys

		for laundry in laundrys['laundrys']:

			#print laundry

			btns = []
			
			postback = 'SELECT_LAUNDRY_ID_%s' %laundry['id']
			button2 = {"type":"postback","title":"Seleccionar","payload": postback}
			btns.append(button2)

			btns.append(button)

			element = json.loads(laundry['desc'])
			element["buttons"] = btns
			payload['message']['attachment']['payload']['elements'].append(element)

			print postback
			
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

	def solicitar_dato(self,dic):
		for id_fb in dic:
			if id_fb == self.clienteFB.idSender():
				return True
		return False




	def pedirDato(self,dic_validador,val):
		if val == True:
			dic_validador[self.clienteFB.idSender()] = "LOCALIDAD"
			self.enviarMensaje(self.preguntas["LOCALIDAD"])
			return
		
		dato = dic_validador[self.clienteFB.idSender()]
		print dato		
		
		if dato == "LOCALIDAD":
			dic_validador[self.clienteFB.idSender()] = "DIRECCION"
			self.enviarMensaje(self.preguntas["DIRECCION"])









