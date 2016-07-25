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

laundry_blueprint = Blueprint(
    'laundry', __name__,
    template_folder='templates'
)  


################
## functions ###
################

def parse_laundrys(res):
        new_res = {"response":{"laundrys":[]}}

        for laundry in res:

                dict_res = {}
                dict_res['id'] = laundry['id']
                dict_res['name'] = laundry['name']
                dict_res['type'] = laundry['type']
                dict_res['desc'] = laundry['desc']
                dict_res['open'] = laundry['open_hs']
                dict_res['close'] = laundry['close_hs']
                dict_res['days'] = laundry['open_days']
                dict_res['address'] = laundry['address']
                dict_res['localidad'] = laundry['localidad']
                dict_res['city'] = laundry['city']
                dict_res['country'] = laundry['country']
                dict_res['user'] = laundry['user_laundry']

                new_res['response']['laundrys'].append(dict_res)

	return new_res['response']


################
#### routes ####
################

#POST para obtener todas las lavanderias filtradas por un parametro que llega en el payload
@laundry_blueprint.route('/getall', methods=['POST'])
def get_all_laundry():
	json = request.get_json(force=True)
        dict_res = {}

	res = service.getAllLaundry(json)

	if res is not None:
		dict_res = parse_laundrys(res)
	else:
		dict_res['response'] = 'error - BAD REQUEST'

	return jsonify(dict_res)	



@laundry_blueprint.route('/ping', methods=['GET']) 
def ping():
	return "Pong"
