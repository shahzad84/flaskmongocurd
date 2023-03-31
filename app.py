from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017"
mongo = PyMongo(app)

ObjectID = ('mongodb').ObjectId;
class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

#the CRUD operations
@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    result = []
    for user in users:
        user_obj = {
            'id': str(user['_id']),
            'name': user['name'],
            'email': user['email'],
            'password': user['password']
        }
        result.append(user_obj)
    return jsonify(result)

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    if user:
        user_obj = {
            'id': str(user['_id']),
            'name': user['name'],
            'email': user['email'],
            'password': user['password']
        }
        return jsonify(user_obj)
    else:
        return jsonify({'error': 'User not found'})

@app.route('/users', methods=['POST'])
def add_user():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    new_user = User(name, email, password)
    user_id = mongo.db.users.insert_one({
        'name': new_user.name,
        'email': new_user.email,
        'password': new_user.password
    }).inserted_id
    return jsonify({'id': str(user_id)})

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    result = mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set': {
        'name': name,
        'email': email,
        'password': password
    }})
    if result.modified_count == 1:
        return jsonify({'message': 'User updated successfully '})
    else:
        return jsonify({'error': 'User not found '})

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    result = mongo.db.users.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 1:
        return jsonify({'message': 'User deleted successfully from data'})
    else:
        return jsonify({'error': 'User not found in data'})

if __name__ == '__main__':
    app.run(debug=True)
