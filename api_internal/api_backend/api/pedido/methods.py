#################
#### imports ####
#################

from flask import render_template, Blueprint, \
    request, flash, redirect, url_for, json, jsonify  # pragma: no cover
from api.database import service
from api.config import Settings
import requests

################
#### config ####
################

pedido_blueprint = Blueprint(
    'pedido', __name__,
    template_folder='templates'
)  


################
## functions ###
################

def parse_pedido(res):
        new_res = {"response":{}}
        new_res['response']['id'] = res['id']
        new_res['response']['user'] = res['user_id']
        new_res['response']['laundry'] = res['laundry_id']
        new_res['response']['payment'] = res['payment_id']
        new_res['response']['delivery'] = res['delivery_id']
        new_res['response']['date'] = res['date_pedido']
        new_res['response']['status'] = res['status']
        new_res['response']['reclamo'] = res['reclamo_id']

        return new_res

################
#### routes ####
################

@pedido_blueprint.route('/new', methods=['POST']) 
def new_pedido():
	json = request.get_json(force=True)
	dict_res = {}

	if service.insertPedido(json):
                dict_res['response'] = 'successful'
        else:
                dict_res['response'] = 'error - the insert fail'

	return jsonify(dict_res)	


#El payload tiene que venir con el nombre del campo por el cual hacer la query. Ejemplo: laundry_id, payment_id, user_id, delivery_id o reclamo_id
@pedido_blueprint.route('/detail', methods=['POST'])
def get_last_pedido():
	json = request.get_json(force=True)
        dict_res = {}
	
	res = service.getPedido(json)

	if res is not None:
		dict_res = parse_pedido(res)
	else:
		dict_res['response'] = 'error - BAD REQUEST'
	
	return jsonify(dict_res)	

#El payload tiene que venir con el pedido_id obligatoriamente y ademas tiene que tener los campos que se quieren updetear de la db
@pedido_blueprint.route('/modify', methods=['POST'])
def modify_pedido():
	json = request.get_json(force=True)
        dict_res = {}	

        if service.modifyPedido(json):
                dict_res['response'] = 'successful'
        else:
                dict_res['response'] = 'error - the insert fail'

        return jsonify(dict_res)			


@pedido_blueprint.route('/ping', methods=['GET']) 
def ping():
	return "Pong"
