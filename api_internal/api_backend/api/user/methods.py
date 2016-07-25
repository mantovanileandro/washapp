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

user_blueprint = Blueprint(
    'user', __name__,
    template_folder='templates'
)  


################
## functions ###
################

def parse_user(res):
	new_res = {"response":{}}
	dict_res = new_res['response']
	dict_res['name'] = res['firstname']
	dict_res['surname'] = res['lastname']
 	dict_res['email'] = res['email']
	dict_res['reg_date'] = res['reg_date']
	dict_res['address'] = res['address']
	dict_res['localidad'] = res['localidad']	
	dict_res['phone'] = res['phone']	
	dict_res['gender'] = res['gender']
	dict_res['fb_id'] = res['user_fb']
	
	return dict_res


################
#### routes ####
################

@user_blueprint.route('/<id>', methods=['GET','POST'])
def existUser(id):
	res = service.getUser(id,'custom')	

	if res is not None:
		res = {'exist':'true'}
	else:
		res = {'exist':'false'}
        
	return jsonify(res)

@user_blueprint.route('/fb/<int:fbId>', methods=['GET','POST'])
def existFacebookUser(fbId):
        res = service.getUser(fbId,'fb')
        
	if res is not None:
                res = {'exist':'true'}
        else:
                res = {'exist':'false'}

	return jsonify(res)


@user_blueprint.route('/<int:id>/detail', methods=['GET','POST'])
def getDetailUser(id):
        res = service.getUser(id,'custom')
	
	dict_res = {}
        if res is not None:
                dict_res = parse_user(res)
        else:
                dict_res['response'] = 'error - the user not exist'
                
	return jsonify(dict_res)


@user_blueprint.route('/fb/<int:fbId>/detail', methods=['GET','POST'])
def getDetailFacebookUser(fbId):	
	res = service.getUser(fbId,'fb')
	
	dict_res = {}
	if res is not None:
        	dict_res = parse_user(res)		
	else:
		dict_res['response'] = 'error - the user not exist'
		
	return jsonify(dict_res)		


@user_blueprint.route('/insert', methods=['POST'])
def insertNewUser():
	json = request.get_json(force=True)
	dict_res = {}

        if service.getUser(json['user_fb'],'fb') is None: 
		res = service.insertUser(json)
		dict_res['response'] = 'successful'
	else:
		dict_res['response'] = 'error - the user already exist'

	return jsonify(dict_res)

@user_blueprint.route('/modify', methods=['POST'])
def modifyUser():
	json = request.get_json(force=True)
	dict_res = {}
	
	if service.getUser(json['user_fb'],'fb') is not None:
		res = service.modifyUser(json)	
		dict_res['response'] = 'successful'
	else:
		dict_res['response'] = 'error - the user not exist'	

	return jsonify(dict_res)
		
@user_blueprint.route('/ping', methods=['GET'])
def ping():
	return "Pong"
