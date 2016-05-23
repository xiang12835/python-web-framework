from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://yuxiang:yuxiang0128@pythontest.cecvfgav3yog.ap-northeast-2.rds.amazonaws.com/pythontest'
db = SQLAlchemy(app)

class UserDB(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(32),unique=True)
    password = db.Column(db.String(32))
    def __init__(self,username,password):
        self.username = username
        self.password = password
    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.id
        except Exception,e:
            db.session.rollback()
            return e
        finally:
            return 0
    def isExisted(self):
        temUser = UserDB.query.filter_by(username=self.username,password=self.password).first()
        if temUser is None:
            return 0
        else:
            return 1

class User(object):
    def __init__(self,user_id,user_name):
        self.user_id = user_id
        self.user_name = user_name
        