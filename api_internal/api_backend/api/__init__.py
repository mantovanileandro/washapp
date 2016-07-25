#################
#### imports ####
#################

from flask import Flask

################
#### config ####
################
def create_app():
	app = Flask(__name__)
	app.config.from_object('api.config.DatabaseConf')

	from api.database import db
	db.app = app
	db.init_app(app)

	from user.methods import user_blueprint
	app.register_blueprint(user_blueprint, url_prefix = '/user')
	from pedido.methods import pedido_blueprint
	app.register_blueprint(pedido_blueprint, url_prefix = '/pedido')	
	from laundry.methods import laundry_blueprint
	app.register_blueprint(laundry_blueprint, url_prefix = '/laundry')

	return app
