import sqlite3
from db import db

class UserModel(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80))
	password = db.Column(db.String(80))

	def __init__(self, username, password):
		self.username = username
		self.password = password

	def json(self):
		return {'id': self.id, 'username': self.username}

	def save_user(self):
		db.session.add(self)
		db.session.commit()

	def delete_user(self):
		db.session.delete(self)
		db.session.commit()

	@classmethod
	def find_by_username(cls, username):
		return cls.query.filter_by(username=username).first()

		# connection = sqlite3.connect('data.db')
		# cursor = connection.cursor()

		# query = 'SELECT * FROM users WHERE username=?'
		# result = cursor.execute(query, (username,)) # input needs to be in tuple format

		# row = result.fetchone()
		# if row:
		# 	user = cls(*row) #row[0], row[1], row[2]
		# else:
		# 	user = None

		# connection.close()
		# return user

	@classmethod
	def find_by_id(cls, _id):
		return cls.query.filter_by(id=_id).first()

		# connection = sqlite3.connect('data.db')
		# cursor = connection.cursor()

		# query = 'SELECT * FROM users WHERE id=?'
		# result = cursor.execute(query, (_id,)) # input needs to be in tuple format

		# row = result.fetchone()
		# if row:
		# 	user = cls(*row) #row[0], row[1], row[2]
		# else:
		# 	user = None

		# connection.close()
		# return user

