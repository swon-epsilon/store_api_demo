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










