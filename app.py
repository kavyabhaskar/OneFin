from flask import Flask, Blueprint, request, jsonify, g, make_response
from flask_cors import CORS, cross_origin
from werkzeug.security import safe_str_cmp
from flask_mongoengine import MongoEngine
from user_schema import User, db
from collections_schema import Collection
from mongoengine import *
import json
from flask_jwt_extended import (jwt_required,
                                create_access_token,
                                JWTManager
)
import requests
import uuid

JWT_SECRET = 'super-secret'
JWT_ALGORITHM = 'HS256'

app = Flask(__name__)

jwt = JWTManager(app)
app.config['SECRET_KEY'] = 'super secrets'

app.config['JWT_SECRET_KEY'] = 'WhyShouldYouEncrypt'

app.config['JWT_BLACKLIST_ENABLED'] = True

app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']



cors = CORS(app)
app.config['PROPAGATE_EXCEPTIONS'] = True


app.config['CORS_HEADERS'] = 'Content-Type'

mongo = MongoEngine()

def create_uuid():
    the_uuid = str(uuid.uuid4())
    return the_uuid


# 1. User Registration
@app.route('/register', methods=['POST'])
@cross_origin()

def register():
    data = request.get_json()
    print(data)
    try:
        username = data['username']
        password = data['password']
        user_dict = {"username" : username,
                    "password":password}
    except:
        message = "Required field is not specified"

    data = user_dict
    data = json.dumps(data)
    print(data)
    user_data = User.from_json(data)
        
    try:  
        user_data.save() # creates a new user in database
        message = "Success, User Registered"
        access_token = create_access_token(identity=username)
        
        return {

                "access_token": access_token
            }
    except:

        return {'message': 'Something went wrong'}


# 2. Paginated list of movies in the third party api. [Api integration is done here]
@app.route('/movies', methods=['GET'])
@cross_origin()
@jwt_required()
def movies():
    url = "https://demo.credy.in/api/v1/maya/movies/"
    user = "iNd3jDMYRKsN1pjQPMRz2nrq7N99q4Tsp9EY9cM0"
    password = "Ne5DoTQt7p8qrgkPdtenTK8zd6MorcCR5vXZIJNfJwvfafZfcOs4reyasVYddTyXCz9hcL5FGGIVxw3q02ibnBLhblivqQTp4BIC93LZHj4OppuHQUzwugcYu7TIC5H1"
    response = requests.get(url, auth=(user, password))
    print(response)
    output1 = response.text
    return output1


# 3. Gets my collection of movies and my top 3 favourite genres based on the movies across all my collections.
@app.route('/collection', methods=['GET'])
@cross_origin()
@jwt_required()
def getall_collection():
    genlist = []
    q_set = Collection.objects()
    json_data = q_set.to_json()
    dicts = json.loads(json_data)
    m = [d['movies'] for d in dicts]
    for x in m:
        new = [d['genres'] for d in x]
        for y in new:
            genlist.append(y)

    favourite_genres = [x for x in genlist if x]
    favourite_genres = favourite_genres[:3]
    
    for x in dicts:
        final_dict = x.pop("movies")

    return { "is true": True,
        "data":{
            "collections":dicts,
            "favourite_genres":favourite_genres}}


# 4. Create new Collection of movies
@app.route('/collection', methods=['POST'])
@cross_origin()
@jwt_required()
def create_collection():
    data = request.get_json()
    uuid = create_uuid()
    description = data['description']
    movies = data["movies"]

    try:
        title = data['title']
        collection_dict = {
            "title":title,
            "description":description,
            "movies":movies,
            "uuid":uuid
        }
    except:
        return  "Title is not specified"

    data = collection_dict
    data = json.dumps(data)
    print(data)
    collection_data = Collection.from_json(data)
    
    try:  
        collection_data.save() # creates a new user in database
        message = "Success, Collection is created"
        return {
                "collection_uuid":uuid
            }
    except:
        return {'message': 'Something went wrong'}


# 5. Update a collection, given collection uuid
@app.route('/collection/<collection_uuid>', methods=['PUT'])
@cross_origin()
@jwt_required()
def update_collection(collection_uuid):
    data = request.get_json()
    try:
        updating_collection = Collection.objects.get(uuid = collection_uuid)
        updating_collection.update(**data)
        
        return {"Success": "Document updated successfully"}
    except:
        return {"Failed":"Error while updating document"}


# 6. Get collection details given uuid
@app.route('/collection/<collection_uuid>', methods=['GET'])
@cross_origin()
@jwt_required()
def get_collection(collection_uuid):
    q_set = Collection.objects(uuid = collection_uuid)
    json_data = q_set.to_json()
    dicts = json.loads(json_data)
    for x in dicts:
        final_dict = x.pop("uuid")
    return {"data":dicts}


# 7. Delete a collection, given collection uuid

@app.route('/collection/<collection_uuid>', methods=['DELETE'])
@cross_origin()
@jwt_required()
def delete_collection(collection_uuid):
    print(collection_uuid)
    collection = Collection.objects(uuid=collection_uuid)
    collection.delete()
    return "success"

if __name__=="__main__":
    app.run(port=8000, debug=True,use_reloader=False)   