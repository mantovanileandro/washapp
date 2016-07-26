import os
import json
import requests
import urllib2
from menusFB import menusFB
from validate import validate
from reqsbackend import reqsbackend


class postback:
        def __init__(self,req,menusFB,validate):
                #self.req = req
                self.event = req['entry'][0]['messaging'][0]

                self.postback = self.event['postback']['payload']
                self.fbid = self.event['sender']['id']

                self.menu = menusFB
                self.validate = validate
                self.req_backend = reqsbackend()


        def derivar_postback(self):

                if self.postback == 'PRINCIPAL_TUTORIAL':
                        self.menu.mostrarTutorial()

                elif self.postback == 'PRINCIPAL_STATUS':
                        self.menu.enviarMensaje("STATUS")

                elif self.postback == 'PRINCIPAL_PEDIDO':
                        if self.req_backend.existeUser(self.fbid):
                                res = self.req_backend.getLastPedido(self.fbid)
                                print res
                                if res != None:
                                        #mostrar laundry
                                        print "mostrar laundry"

                                        #obtener la location del usuario
                                        location = self.req_backend.getUserLocation()
                                        #obtener todas las lavanderias para esa location
                                        laundrys = self.req_backend.getAllLaundrys(location)
                                        #armar el payload con las lavanderias (mostrar menu)
                                        self.menu.mostrarLaundrys(laundrys)
                                else:
                                        #mostrar repetir_pedido
                                        print "mostrar repetir_pedido"
                        else:
                                self.menusFB.pedirDato(self.fbid,"INICIA")

                elif self.postback == "TUTORIAL_VOLVER":
                        self.menu.menu_principal()
