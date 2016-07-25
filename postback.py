import os
import json
import requests
import urllib2
from menusFB import menusFB


class postback:
        def __init__(self,req,menusFB):
                #self.req = req
                self.postback = req['payload']
                self.menu = menusFB


        def derivar_postback(self):

                if self.postback == 'PRINCIPAL_TUTORIAL':
                        self.menu.mostrarTutorial()

                elif self.postback == 'PRINCIPAL_STATUS':
                        self.menu.enviarMensaje("STATUS")

                elif self.postback == 'PRINCIPAL_PEDIDO':
                        self.menu.verificarDatos()

                elif self.postback == "TUTORIAL_VOLVER":
                        self.menu.menu_principal()
