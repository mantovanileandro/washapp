from api import create_app
from api.config import Settings

if __name__ == '__main__':
   	app = create_app()

   	settings = Settings()
   	HOST = settings.parameter['HOST']
   	PORT = settings.parameter['PORT']
	
#	app.debug = True   	
   	app.run(threaded = True, host = HOST, port = PORT)
