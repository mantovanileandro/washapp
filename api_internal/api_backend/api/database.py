from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

class Service:
        def __init__(self, database):
                self.database = database

        def getUser(self,id,scope):
                if scope == 'fb':
                        cmd = "SELECT * FROM Users WHERE user_fb = :id"
                elif scope == 'custom':
                        cmd = "SELECT * FROM Users WHERE id = :id"

                user = db.session.execute(cmd, {'id':id}).first()
                if user:
                        return user
                else:
                        return None

        def insertUser(self,profile):
                #################
                ### INIT VARS ###
                ################
                dict_profile = {'address':None, 'localidad': None, 'phone': None, 'email': None, 'gender':profile['gender'], 'user_fb':profile['user_fb'], 'name': profile['firstname'], 'surname': profile['lastname']}

                if profile.has_key('address'):
                        profile_address = profile['address']
                        dict_profile['address'] = profile_address['address']
                        dict_profile['localidad'] = profile_address['localidad']

                if profile.has_key('phone'):
                        dict_profile['phone'] = profile['phone']

                if profile.has_key('email'):
                        dict_profile['email'] = profile['email']

                cmd = 'INSERT INTO Users (firstname,lastname,email,reg_date,address,localidad,phone,gender,user_fb) VALUES (:name,:surname,:email,NOW(),:address,:localidad,:phone,:gender,:user_fb)'
                res = db.session.execute(cmd, dict_profile)
                db.session.commit()


        def modifyUser(self,profile):
                cmd = 'UPDATE Users SET '
                c = 0
                dict_profile = {}
                user_fb = profile['user_fb']
                del profile['user_fb']

                for key in profile.keys():
                        cmd += ' %s=:v%i,' %(key,c)
                        str = 'v%i' %c
                        dict_profile[str] = profile[key]
                        c += 1

                cmd = cmd[:-1]
                cmd += ' WHERE user_fb = %s' %user_fb

                try:
                        res = db.session.execute(cmd, dict_profile)
                        db.session.commit()
                        return True
                except:
                        return False

        def insertPedido(self,pedido):
                dict_profile = {"laundry_id": None, "delivery_id": None, "payment_id": None, "status": None, "reclamo_id": None, "status": "new"}

                if pedido.has_key('user_fb'):
                        res = self.getUser(pedido['user_fb'],'fb')
                        if res:
                                dict_profile['user_id'] = res['id']
                elif pedido.has_key('user'):
                        dict_profile['user_id'] = pedido['user']
                else:
                        print 'ERROR - BAD KEY'

                if pedido.has_key('laundry'): dict_profile['laundry_id'] = pedido['laundry']
                if pedido.has_key('delivery'): dict_profile['delivery_id'] = pedido['delivery']
                if pedido.has_key('payment'): dict_profile['payment_id'] = pedido['payment']
                if pedido.has_key('status'): dict_profile['status'] = pedido['status']
                if pedido.has_key('reclamo'): dict_profile['reclamo_id'] = pedido['reclamo']

                cmd = 'INSERT INTO Pedidos (user_id,laundry_id,delivery_id,payment_id,date_pedido,status,reclamo_id) VALUES (:user_id,:laundry_id,delivery_id,payment_id,NOW(),:status,:reclamo_id)'

                try:
                        res = db.session.execute(cmd, dict_profile)
                        db.session.commit()
                        return True
                except:
                        return False


        def getPedido(self,pedido):

                key = pedido.keys()[0]
                cmd = "SELECT * FROM Pedidos WHERE %s = :field_value" %key
                dict_profile = {'field_value':pedido[key]}


                res = db.session.execute(cmd, dict_profile).first()
                return res


        def modifyPedido(self,pedido):

                cmd = 'UPDATE Pedidos SET'

                dict_profile = {}
                c = 0

                pedido_id = pedido['pedido_id']
                del pedido['pedido_id']


                for key in pedido.keys():
                    cmd += ' %s=:v%i,' %(key,c)
                    dict_profile['v%i' %c] = pedido[key]
                    c += 1

                cmd = cmd[:-1]
                cmd += ' WHERE id = %s' %pedido_id

                try:
			res = db.session.execute(cmd, dict_profile)
                	db.session.commit()
               		return True
                except:
                        return False


        def getAllLaundry(self,laundry):

                key = laundry.keys()[0]
                cmd = "SELECT * FROM Laundrys WHERE %s = :field_value" %key
                dict_profile = {'field_value':laundry[key]}

                res = db.session.execute(cmd, dict_profile).fetchall()
                return res





db = SQLAlchemy()
service = Service(db)
