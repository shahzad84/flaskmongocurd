from flask import Flask, request
from flask_restful import Resource, Api
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/users_db'
api = Api(app)
mongo = PyMongo(app)


class User(Resource):
    def get(self, user_id=None):
        if user_id:
            user = mongo.db.users.find_one_or_404({'_id': user_id})
            return {'id': str(user['_id']), 'name': user['name'], 'email': user['email']}
        else:
            users = mongo.db.users.find()
            result = []
            for user in users:
                result.append(
                    {'id': str(user['_id']), 'name': user['name'], 'email': user['email']})
            return result

    def post(self):
        data = request.get_json()
        user = {'name': data['name'], 'email': data['email']}
        mongo.db.users.insert_one(user)
        return {'message': 'User created successfully.'}

    def put(self, user_id):
        data = request.get_json()
        user = {'name': data['name'], 'email': data['email']}
        mongo.db.users.update_one({'_id': user_id}, {'$set': user})
        return {'message': 'User updated successfully.'}

    def delete(self, user_id):
        mongo.db.users.delete_one({'_id': user_id})
        return {'message': 'User deleted successfully.'}


api.add_resource(User, '/users', '/users/<ObjectId:user_id>')

if __name__ == '__main__':
    app.run(debug=True)
