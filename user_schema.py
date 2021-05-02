from mongoengine import *
import datetime as dt

db = connect(host = 'mongodb+srv://Kavya:kavya123@cluster0.f1ve8.mongodb.net/Onefin?retryWrites=true&w=majority')
    


class User(Document):
    username = StringField(required=True)
    password = StringField(required=True)