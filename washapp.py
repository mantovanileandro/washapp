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
from validate import validate

app = Flask(__name__)


url_send = 'https://graph.facebook.com/v2.6/me/messages?access_token='

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

	event = checkEvent(res).get_event()
	menu = menusFB(url_send,os.environ['TOKEN'],res)
	validate_obj = validate(url_send,os.environ['TOKEN'],res)

	if event is 'postback':
		postback_obj = postback(res['entry'][0]['messaging'][0]['postback'],menu,validate_obj)
		postback_obj.derivar_postback()
	elif event is 'message':
		if menu.contieneTexto('menu'):
			menu.menu_principal()
	else:
		print "error event"

	return "asd"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
