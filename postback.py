import os
import json
import requests
import urllib2
from menusFB import menusFB
from validate import validate


class postback:
        def __init__(self,req,menusFB,validate):
                #self.req = req
                self.postback = req['payload']
                self.menu = menusFB
                self.validate = validate



        def derivar_postback(self):

                if self.postback == 'PRINCIPAL_TUTORIAL':
                        self.menu.mostrarTutorial()

                elif self.postback == 'PRINCIPAL_STATUS':
                        self.menu.enviarMensaje("STATUS")

                elif self.postback == 'PRINCIPAL_PEDIDO':
                        if self.validate.existe():
                                print "existe"

                        else:
                                print "no existe"

                elif self.postback == "TUTORIAL_VOLVER":
                        self.menu.menu_principal()
