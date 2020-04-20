import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required, 
								create_access_token, 
								create_refresh_token, 
								jwt_refresh_token_required, 
								get_jwt_identity,
								get_raw_jwt)
from werkzeug.security import safe_str_cmp

from models.user import UserModel
from blacklist import black_list

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
						  type=str,
						  required=True,
						  help='This field cannot be left blank')
_user_parser.add_argument('password',
						  type=str,
						  required=True,
						  help='This field cannot be left blank')

class UserRegister(Resource):
	
	def post(self):
		data = _user_parser.parse_args()

		if UserModel.find_by_username(data['username']):
			return {'message': 'A user with that user name already exists'}, 400

		user = UserModel(**data) # UserModel(data['username'], data['password'])
		user.save_user()

		# connection = sqlite3.connect('data.db')
		# cursor = connection.cursor()

		# create_user_query = 'INSERT INTO users VALUES (NULL, ?, ?)'
		# cursor.execute(create_user_query, (data['username'], data['password'],))

		# connection.commit()
		# connection.close()

		return {'message': 'User created successfully.'}, 201 # Created


class User(Resource):
	@classmethod
	def get(cls, user_id):
		user = UserModel.find_by_id(user_id)
		if not user:
			return {'message': 'User not found'}, 404
		return user.json()
	
	@classmethod
	def delete(cls, user_id):
		user = UserModel.find_by_id(user_id)
		if not user:
			return {'message': 'User not found'}, 404
		user.delete_user()
		return {'message': "User with user id: '{}' has been deleted".format(user_id)}, 200


class UserList(Resource):
	def get(self):
		return {'users': [user.json() for user in UserModel.find_all()]}


class UserLogin(Resource):
	@classmethod
	def post(cls):
		data = _user_parser.parse_args()
		user = UserModel.find_by_username(data['username'])

		if user and safe_str_cmp(user.password, data['password']):
			access_token = create_access_token(identity=user.id, fresh=True) # fresh=True - User just logged in with credential
			refresh_token = create_refresh_token(user.id)
			return {'access_token': access_token, 'refresh_token': refresh_token}, 200
		return {'message': 'Invalid credentials'}, 401

class UserLogout(Resource):
	@jwt_required
	def post(self):
		# jwt ID, a unique identifier for a JWT
		jti = get_raw_jwt()['jti']
		black_list.add(jti)
		return {'message': 'Successfully logged out.'}, 200

class TokenRefresh(Resource):
	@jwt_refresh_token_required
	def post(self):
		current_user = get_jwt_identity()
		new_token = create_access_token(identity=current_user, fresh=False)
		return {'access_token': new_token}, 200