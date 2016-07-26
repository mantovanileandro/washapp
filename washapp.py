from flask import Flask
from flask import request
import flask
import os
import json
import requests
import urllib2
from menusFB import menusFB
from checkEvent import checkEvent
from postback import postback
from reqsbackend import reqsbackend
from validate import validate
from reqFB import reqFB

app = Flask(__name__)

dic_validador = {}
url_send = 'https://graph.facebook.com/v2.6/me/messages?access_token='
url_user_datos = 'https://graph.facebook.com/v2.6/<USER_ID>?fields=first_name,last_name,gender&access_token='



@app.route('/test', methods=['GET'])
def washapp():
	return "ESTOY VIVOoooooooo"




@app.route('/webhook', methods=['GET'])
def validate_token():
	token = os.environ['TOKEN']
	verify_token = request.args["hub.verify_token"]
	if verify_token == token:
		return request.args['hub.challenge']
	else:
		return "Invalid verify token"





@app.route('/webhook', methods=['POST'])
def webhook():
	res = request.get_json(silent=True)

	req_fb = reqFB(res)
	event = checkEvent(res).get_event()
	menu = menusFB(url_send,os.environ['TOKEN'],res)
	req_backend = reqsbackend()
	validate_obj = validate(url_send,os.environ['TOKEN'],res)

	if event is 'postback':
		postback_obj = postback(res,menu,validate_obj,dic_validador)
		postback_obj.derivar_postback()

	elif event is 'message':
		if menu.solicitar_dato(dic_validador):
			menu.pedirDato(dic_validador,False)
		if menu.contieneTexto('menu'):
			menu.menu_principal()

	elif event is 'optin':
		if not req_backend.existeUser(res['sender']['id']):
			url = url_user_datos.replace('<USER_ID>', res['sender']['id']) + os.environ['TOKEN']
			datos_user = request.get(url)
			datos_user['user_fb'] = res['sender']['id']
			req_backend.crearUser(datos_user)

	else:
		print "error event"

	return "asd"






if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
