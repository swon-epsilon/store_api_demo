import os

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from resources.user import UserRegister, User
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') # 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = '4ckf4fm2'
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth

# items = []

api.add_resource(UserRegister, '/register').
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserList, '/users')

api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1:5000/student/Sam
api.add_resource(ItemList, '/items')

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__': # this prevents app.run() from running when app.py is imported from other files.
	app.run(port=5000, debug=True) 

# Common Status Code List
# 200 OK
# 201 Created
# 202 Accepted (delaying creation for a process that may take longer to process / client does not have to wait)
# 400 Bad Request
# 401 Unauthorized
# 404 Not Found
# 500 Internal Server Error