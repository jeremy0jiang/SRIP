from app import db
from datetime import datetime

class User(db.Model) :
    __tablename__ = 'users'
            
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(12), nullable=False)
    src = db.Column(db.String(100), nullable=False)
                                
    def __init__(self, username, password,src):
        self.username = username
        self.password = password
        self.src = src

class Message(db.Model) :
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    time = db.Column(db.DateTime)
   

    def __init__(self,text,username):
        self.text = text
        self.username = username
        self.time = datetime.utcnow()



