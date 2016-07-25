from flask import Flask
from flask import request
import flask
import os
import json
import requests
import urllib2
from menusFB import menusFB

app = Flask(__name__)


url_send = 'https://graph.facebook.com/v2.6/me/messages?access_token='

@app.route('/test', methods=['GET'])
def washapp():
	return "ESTOY VIVOoooooooo"


@app.route('/webhook', methods=['GET'])
def validate():
	token = os.environ['TOKEN']
	verify_token = request.args["hub.verify_token"]
	if verify_token == token:
		return request.args['hub.challenge']
	else:
		return "Invalid verify token"		

def send_principal_menu(userId):
	payload = {}
	payload['recipient'] = {"id":userId}
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

	url = url_send + os.environ['TOKEN']
	res = requests.post(url,json=payload)

def send_principal_tutorial(userId):
        payload = {}
        payload['recipient'] = {"id":userId}
	payload['message'] = {"attachment":{}}
	payload['message']['attachment']['type'] = 'template'
	payload['message']['attachment']['payload'] = {}
	payload['message']['attachment']['payload']['template_type'] = 'generic'
	payload['message']['attachment']['payload']['elements'] = []
	element = {"title": "rift","subtitle": "Next-generation virtual reality","image_url": "http://messengerdemo.parseapp.com/img/rift.png"}
	payload['message']['attachment']['payload']['elements'].append(element)
	element = {"title": "rift","subtitle": "Next-generation virtual reality","image_url": "http://messengerdemo.parseapp.com/img/rift.png"}
        payload['message']['attachment']['payload']['elements'].append(element)	
	
	url = url_send + os.environ['TOKEN']
        res = requests.post(url,json=payload)

def send_message(senderId,text):
	payload = {"recipient": {"id":senderId},"message": {"text":text}}
	url = url_send + os.environ['TOKEN']
	res = requests.post(url,json=payload)

# def principal_pedido():
# 	#chequear que el user exista y que tenga los datos cargados (api backend)
# 	res = requests.get(api_backend,params)
# 	if res is None:
# 		#cargar datos
# 		#select laundry
# 		#select horario
# 	else:
# 		#chequear si ya hizo un pedido anteriormente
# 		res = requests.get(api_backend,params)
# 		if res is None:
# 			#select laundry
# 		else:
# 			#repetir laundry
		


def postback_deriv(request):
	postback = request['postback']['payload']
	
	if postback == 'PRINCIPAL_TUTORIAL': send_principal_tutorial(request['sender']['id'])
	elif postback == 'PRINCIPAL_STATUS':
		print "asd"
		#return status
	elif postback == 'PRINCIPAL_PEDIDO':
		print "asd"
		#flujo de pedido

@app.route('/webhook', methods=['POST'])
def webhook():
	menu = menusFB(url_send,os.environ['TOKEN'])
	res = request.get_json(silent=True)['entry'][0]['messaging']
	respuestacompleta = request.get_json(silent=True)
	print res
	for req in res:
		if req.has_key('message'): 
			if req['message'].has_key('text'):
				if req['message']['text'].lower() == 'menu':
					#send_message(message['sender']['id'],message['message']['text'])
					menu.menu_principal(respuestacompleta)
		elif req.has_key('postback'):
			postback_deriv(req)	

	return 'asd'

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)