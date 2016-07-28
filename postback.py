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


        def mostrar_laundrys(self,scope):
                #mostrar laundrys

                #obtener la location del usuario
                location = self.req_backend.getUserLocation(self.fbid)
                #obtener todas las lavanderias para esa location
                res = self.req_backend.getAllLaundrys(location)

                if res != None:
                        laundrys = res['response']
                        #aca puedo pasar el algoritmo de ordenamiento y filtrado de laundrys
                        self.menu.mostrarLaundrys(laundrys,scope)
                else:
                        print "no hay laundrys disponibles"


        def derivar_postback(self):

                #####################################
                ###### POSTBACK MENU PRINCIPAL ######
                #####################################


                if self.postback == 'PRINCIPAL_TUTORIAL':
                        self.menu.mostrarTutorial()

                elif self.postback == 'PRINCIPAL_STATUS':
                        usuario = self.req_backend.estaCompleto(self.fbid)
                        print usuario
                        self.menu.enviarMensaje("STATUS")

                elif self.postback == 'PRINCIPAL_PEDIDO':
                        
                        if self.req_backend.estaCompleto(self.fbid) == "[]":
                                last_pedido = self.req_backend.getLastPedidoByUser(self.fbid) #arreglar esto para que devuelva el ultimo pedido (ordenar por fecha)

                                if last_pedido is None:
                                        self.mostrar_laundrys('PRINCIPAL')
                                else:
                                        #mandarlo a que termine de completar el flujo
                                        if 'select_laundry' in last_pedido['status']:
                                                #mandarlo a que elija el horario
                                                print "elejir horario"
                                        elif 'select_horario' in last_pedido['status']:
                                                #mandarlo a que complete el pago
                                                print "completar pago"
                                        else:
                                                last_completed_pedido = self.req_backend.getLastPedidoByStatus('completed')

                                                if last_completed_pedido is not None:
                                                        self.menu.mostrarRepetirPedido()
                                                else:
                                                        self.mostrar_laundrys('PRINCIPAL')

                        else:
                                print "ENTRO AL ELSE"
                                self.menu.pedirDato()


                #####################################
                ##### POSTBACK ALL MENUS VOLVER #####
                #####################################

                elif self.postback == "TUTORIAL_VOLVER":
                        self.menu.menu_principal()
                elif self.postback == 'SELECT_LAUNDRY_VOLVER':
                        self.menu.menu_principal()


                #####################################
                ###### POSTBACK SELECT LAUNDRY ######
                #####################################

                elif 'SELECT_LAUNDRY_PRINCIPAL_ID_' in self.postback:

                        laundry_id = self.postback.split('_')[-1]
                        res = self.req_backend.setNewPedido(self.fbid, laundry_id)

                        if res:
                                print "seleccionar horario"
                        else:
                                print "hubo un error al insertar la lavanderia"


                elif 'SELECT_LAUNDRY_CAMBIAR_LAUNDRY_ID_' in self.postback:

                        laundry_id = self.postback.split('_')[-1]
                        res = self.req_backend.setNewPedido(self.fbid, laundry_id)

                        if res:
                                print "completar pedido"
                        else:
                                print "hubo un error al insertar la lavanderia"


                #####################################
                ###### POSTBACK REPETIR PEDIDO ######
                #####################################

                elif self.postback == 'PEDIDO_REPETIR_QUICK_REPLIE_YES':
                        #repetir todo el pedido anterior
                        print "repetir pedido entero"

                elif self.postback == 'PEDIDO_REPETIR_QUICK_REPLIE_NO':
                        #mostrarle las lavanderias
                        self.mostrar_laundrys('PRINCIPAL')

                elif self.postback == 'PEDIDO_REPETIR_QUICK_REPLIE_CAMBIAR_LAUNDRY':
                        #mostrarle solo las lavanderias y desp mandarlo a terminar el pedido
                        print "repetir pedido cambiar laundry"
                        self.mostrar_laundrys('CAMBIAR_LAUNDRY')

                elif self.postback == 'PEDIDO_REPETIR_QUICK_REPLIE_CAMBIAR_HORARIO':
                        #mostrarle solo los horarios y desp mandarlo a terminar el pedido
                        print 'mostrar horarios y completar pedido'







