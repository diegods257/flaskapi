from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS
from dotenv import load_dotenv
from os import environ


#REST API

load_dotenv()
app = Flask(__name__)  # inicializar la clase Flask



user = environ.get('USER')
password = environ.get('PASSWORD')
cluster = environ.get('CLUSTER')
collection = environ.get('COLLECTION')
app.config['MONGO_URI'] = f'mongodb+srv://{user}:{password}@{cluster}.ognohgc.mongodb.net/{collection}?retryWrites=true&w=majority'
mongo = PyMongo(app)

CORS(app)

db = mongo.db.users




@app.route('/matriculas', methods=['POST'])
def createUser():

    print(request.json)
    id = db.insert_one({'name': request.json['name'], 'email': request.json['email'], 'asignatura': request.json['asignatura'], 'creditos': request.json['creditos']
                    })

    print(id.inserted_id) #para mostrar el objeto en string, retorna el id
    
    return jsonify(str(id.inserted_id))



@app.route('/matriculas', methods=['GET'])
def getUsers():
    users = []
    print(db.find())
    for doc in db.find():
        users.append({
            '_id': str(ObjectId(doc["_id"])),
            'name': doc['name'],
            'email': doc['email'],
            'asignatura': doc['asignatura'],
            'creditos': doc['creditos']
        })
    print(users)    
    return jsonify(users)


@app.route('/matriculas/<id>', methods=['GET'])
def getUser(id):
    print(id)
    user = db.find_one({'_id': ObjectId(id)}) #convertir el id a object
    print(user) #user tiene como propiedad _id que es de tipo ObjectId, se debe convertir a un string 
    return jsonify({
            '_id': str(ObjectId(user["_id"])),
            'name': user['name'],
            'email': user['email'],
            'asignatura': user['asignatura'],
            'creditos': user['creditos']
        })


@app.route('/matriculas/<id>', methods=['DELETE'])
def deleteUser(id):
    print(id)
    respuesta = db.delete_one({'_id': ObjectId(id)}) 
    print(respuesta)
    return jsonify({"message": "Usuario eliminado"})


@app.route('/matriculas/<id>', methods=['PUT'])
def updateUser(id): 
    print(request.json) #update only works with $ operators
    db.update_one({"_id": ObjectId(id)}, {'$set': {'name': request.json['name'], 'email': request.json['email'], 'asignatura': request.json['asignatura'], 'creditos': request.json['creditos']}
                                                 })
    return jsonify({"message": "Usuario actualizado"})



if __name__ == "__main__":
    app.run(debug=False)  #desactivar en produccion
