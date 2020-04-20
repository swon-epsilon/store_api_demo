import os

from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager # JWT, jwt_required

# from security import authenticate, identity
from resources.user import UserRegister, User, UserList, UserLogin, UserLogout, TokenRefresh
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from blacklist import black_list

# from db import db

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_SECRET_KEY'] = '4ckf4fm2&U'
app.secret_key = '4ckf4fm2'
api = Api(app)

# items = []

# @app.before_first_request
# def create_tables():
# 	db.create_all()

jwt = JWTManager(app) # /login # /auth

@jwt.user_claims_loader # link to JWTManager
def add_claims_to_jwt(identity):
	if identity == 1:
		return {'is_admin': True}
	return {'is_admin': False}

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
	return decrypted_token['jti'] in black_list

@ jwt.expired_token_loader
def expired_token_callback():
	return jsonify({'description': 'The token has expired.',
					'error': 'token_expired'}), 401	

@jwt.invalid_token_loader
def invalid_token_callback(error):
	return jsonify({
		'description': 'Signature verification failed.',
		'error': 'invalid_token'
		}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
	return jsonify({
		'description': 'Request does not contain an access token.',
		'error': 'authorization_required'
		}), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
	return jsonify({
		'description': 'The token is not fresh.',
		'error': 'fresh_token_required'
		}), 401

@jwt.revoked_token_loader
def revoked_token_callback():
	return jsonify({
		'description': 'The token has been revoked.',
		'error': 'token_revoked'
		}), 401

api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserList, '/users')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')

api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1:5000/student/Sam
api.add_resource(ItemList, '/items')

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__': # this prevents app.run() from running when app.py is imported from other files.
	# db.init_app(app)
	app.run(port=5000, debug=True) 

# Common Status Code List
# 200 OK
# 201 Created
# 202 Accepted (delaying creation for a process that may take longer to process / client does not have to wait)
# 400 Bad Request
# 401 Unauthorized
# 404 Not Found
# 500 Internal Server Error