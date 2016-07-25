import os

class Password(object):
  def __init__(self):
    self.db_user = os.environ.get('DB_WASHAPP_USER')
    self.db_pass = os.environ.get('DB_WASHAPP_PWD')


class Config(object):
    p = Password()
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'mysql://' + p.db_user + ':' + p.db_pass + '@config-rds.cltwrgnnvmg2.us-west-1.rds.amazonaws.com:3306/config'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DatabaseConf(Config):
    p = Password()
    SQLALCHEMY_DATABASE_URI = 'mysql://' + p.db_user + ':' + p.db_pass + '@config-rds.cltwrgnnvmg2.us-west-1.rds.amazonaws.com:3306/config'

class Settings(object):
	
  def __init__(self):
    p = Password()
    self.parameter = {
      "HOST": "0.0.0.0",
      "PORT": 80}
