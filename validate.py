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

	def existe(self):
		res = self.reqsbackend.existeUser(self.clienteFB.idSender())
		print res
		return res
