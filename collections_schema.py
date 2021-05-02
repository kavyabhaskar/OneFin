from mongoengine import *
import datetime as dt

db = connect(host = 'mongodb+srv://Kavya:kavya123@cluster0.f1ve8.mongodb.net/Onefin?retryWrites=true&w=majority')
    

class Movies(EmbeddedDocument):
    title = StringField(required=True)
    description = StringField()
    genres = StringField()
    uuid = StringField()

class Collection(Document):
    title = StringField(required=True)
    description = StringField()
    uuid = StringField()
    movies = ListField(EmbeddedDocumentField(Movies),default=list)
    
