import os
import json
import requests
import urllib2
from reqsFB import reqsFB
from reqsbackend import reqsbackend



class validate:
	def __init__(self,url,token,req):
		self.url = url + token
		self.clienteFB = reqsFB(req)
		self.req = req
		self.reqbackend = reqsbackend()
		

	def verificarDatos(self):
		datosfaltantes = []
		datosfaltantes = self.reqbackend.estaCompleto(self.clienteFB.idSender())
		if len(datosfaltantes) != 0:
			self.enviarMensaje("No tenes los datos cargados :( ")
			for dato in datosfaltantes:
				self.enviarMensaje("me indicarias tu %s :" %dato )
