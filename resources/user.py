import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('username',
						type=str,
						required=True,
						help='This field cannot be left blank')
	parser.add_argument('password',
						type=str,
						required=True,
						help='This field cannot be left blank')

	def post(self):
		data = UserRegister.parser.parse_args()

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
		user = UserModel.find_by_username(user_id)
		if not user:
			return {'message': 'User not found'}, 404
		return user.json()
	
	@classmethod
	def delete(cls, user_id):
		user = UserModel.find_by_username(user_id)
		if not user:
			return {'message': 'User not found'}, 404
		user.delete_user()
		return {'message': "User with user id: '{}' has been deleted".format(user_id)}, 200


class UserList(Resource):
	def get(self):
		return {'users': [user.json() for user in UserModel.find_all()]}





