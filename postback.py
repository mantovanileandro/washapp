import os
import json
import requests
import urllib2
from menusFB import menusFB
from validate import validate
from reqsbackend import reqsbackend


class postback:
        def __init__(self,req,menusFB,validate,dic_validador):
                #self.req = req
                self.event = req['entry'][0]['messaging'][0]

                self.postback = self.event['postback']['payload']
                self.fbid = self.event['sender']['id']

                self.menu = menusFB
                self.validate = validate
                self.req_backend = reqsbackend()
                self.dic_validador = dic_validador


        def derivar_postback(self):

                if self.postback == 'PRINCIPAL_TUTORIAL':
                        self.menu.mostrarTutorial()

                elif self.postback == 'PRINCIPAL_STATUS':
                        self.menu.enviarMensaje("STATUS")

                elif self.postback == 'PRINCIPAL_PEDIDO':
                        print self.req_backend.existeUser(self.fbid)
                        if self.req_backend.existeUser(self.fbid) == "True":
                                res = self.req_backend.getLastPedido(self.fbid)

                                if res is None:
                                        #mostrar laundry
                                        print "mostrar laundry"

                                        #obtener la location del usuario
                                        location = self.req_backend.getUserLocation(self.fbid)
                                        #obtener todas las lavanderias para esa location
                                        res = self.req_backend.getAllLaundrys(location)
                                        print res
                                        if res != None:
                                                laundrys = res['response']
                                                self.menu.mostrarLaundrys(laundrys)
                                        else:
                                                print "no hay laundrys disponibles"
                                        #armar el payload con las lavanderias (mostrar menu)
                                        
                                else:
                                        #mostrar repetir_pedido
                                        print "mostrar repetir_pedido"
                        else:
                                print "ENTRO AL ELSE"
                                self.menu.pedirDato(self.dic_validador,True)

                elif self.postback == "TUTORIAL_VOLVER":
                        self.menu.menu_principal()
