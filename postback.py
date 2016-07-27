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


        def mostrar_laundrys(self):
                #mostrar laundrys

                #obtener la location del usuario
                location = self.req_backend.getUserLocation(self.fbid)
                #obtener todas las lavanderias para esa location
                res = self.req_backend.getAllLaundrys(location)

                if res != None:
                        laundrys = res['response']
                        #aca puedo pasar el algoritmo de ordenamiento y filtrado de laundrys
                        self.menu.mostrarLaundrys(laundrys)
                else:
                        print "no hay laundrys disponibles"


        def derivar_postback(self):

                if self.postback == 'PRINCIPAL_TUTORIAL':
                        self.menu.mostrarTutorial()

                elif self.postback == 'PRINCIPAL_STATUS':
                        self.menu.enviarMensaje("STATUS")

                elif self.postback == 'PRINCIPAL_PEDIDO':
 
                        if self.req_backend.existeUser(self.fbid) == "True":
                                last_pedido = self.req_backend.getLastPedidoByUser(self.fbid) #arreglar esto para que devuelva el ultimo pedido (ordenar por fecha)
                                print last_pedido
                                print self.fbid

                                if last_pedido is None:

                                        self.mostrar_laundrys()
                                        
                                else:
                                        #mostrar repetir_pedido
                                        print "mostrar repetir_pedido"

                                        #mandarlo a que termine de completar el flujo
                                        if last_pedido['status'] is 'select_laundry':
                                                #mandarlo a que elija el horario
                                                print "elejir horario"
                                        elif last_pedido['status'] is 'select_horario':
                                                #mandarlo a que complete el pago
                                                print "completar pago"
                                        else:
                                                print "entro al else"
                                                last_completed_pedido = self.req_backend.getLastPedidoByStatus('completed')

                                                if last_completed_pedido is not None:
                                                        self.menu.mostrarRepetirPedido()
                                                        print 'repetir pedido'
                                                else:
                                                        self.mostrar_laundrys()
                                                        print 'laundrys porque no tengo un menu completo'

                        else:
                                print "ENTRO AL ELSE"
                                self.menu.pedirDato(self.dic_validador,True)

                elif self.postback == "TUTORIAL_VOLVER":
                        self.menu.menu_principal()
                elif self.postback == 'SELECT_LAUNDRY_VOLVER':
                        self.menu.menu_principal()
                elif 'SELECT_LAUNDRY_ID_' in self.postback:
                        laundry_id = self.postback.split('_')[-1]
                        print self.postback
                        print laundry_id
                        res = self.req_backend.setNewPedido(self.fbid, laundry_id)
                        print res
                        if res:
                                #mostrar seleccionar horario
                                print "seleccionar horario"
                        else:
                                print "hubo un error al insertar la lavanderia"







