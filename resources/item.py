import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims

from models.item import ItemModel

class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('price', 
						type=float, 
						required=True, 
						help='This field cannot be left blank')
	parser.add_argument('store_id', 
						type=int, 
						required=True, 
						help='Every item needs a store id')

	@jwt_required
	def get(self, name):
		item = ItemModel.find_by_name(name)

		if item:
			return item.json() # item

		return {'message': 'Item not found'}, 404

		# item = next(filter(lambda x: x['name'] == name, items), None)
		# return {'item': item}, 200 if item else 404

	@jwt_required
	def post(self, name):
		if ItemModel.find_by_name(name):
			return {'message': "An item with name '{}' already exists.".format(name)}, 400

		# if next(filter(lambda x: x['name'] == name, items), None):
		# 	return {'message': "An item with name '{}' already exists.".format(name)}, 400

		# data = request.get_json() # force=True, silent=True
		data = Item.parser.parse_args()
		item = ItemModel(name, **data) # ItemModel(name, data['price']) # {'name': name,'price': data['price']}

		try:
			item.save_to_db() # ItemModel.insert(item) # items.append(item)
		except:
			return {'message': "An error occurred inserting the item."}, 500
		
		return item.json(), 201 # item, 201

	@jwt_required
	def delete(self, name):
		claims = get_jwt_claims()
		if not claims['is_admin']:
			return {'message': 'Admin privilege required.'}, 401

		item = ItemModel.find_by_name(name)
		if item:
			item.delete_from_db()
			return {'message': "Item: '{}' deleted.".format(name)}, 200
		return {'message': "Item: '{}' not found.".format(name)}, 404 

		# connection = sqlite3.connect('data.db')
		# cursor = connection.cursor()

		# query = "DELETE FROM items WHERE name=?"
		# result = cursor.execute(query, (name,))

		# connection.commit()
		# connection.close()
		# global items 
		# items = list(filter(lambda x: x['name'] != name, items))

	@jwt_required
	def put(self, name):
		data = Item.parser.parse_args()
		item = ItemModel.find_by_name(name) # item = next(filter(lambda x: x['name'] == name, items), None)
		# updated_item = ItemModel(name, data['price']) # {'name': name, 'price': data['price']}

		if item:
			item.price = data['price']
		else:
			item = ItemModel(name, **data)

		# if item is None:
		# 	item = ItemModel(name, data['price'])
			# try:
			# 	updated_item.insert() # ItemModel.insert(updated_item) # itmes.append(item)
			# except:
			# 	return {'message': "An error occurred inserting the item."}, 500
		# else:
			# item.price = data['price']
			# try:
			# 	updated_item.update() # ItemModel.update(updated_item)
			# except:
			# 	return {'message': "An error occurred updating the item."}, 500

		item.save_to_db()
		
		return item.json(), 201 # updated_item.json(), 201 # updated_item, 201


class ItemList(Resource):
	@jwt_required
	def get(self):
		return {'items': [item.json() for item in ItemModel.find_all()]}
		# return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}

		# connection = sqlite3.connect('data.db')
		# cursor = connection.cursor()

		# query = "SELECT * FROM items"
		# result = cursor.execute(query)

		# items = []
		# for row in result:
		# 	items.append({'name': row[0], 'price': row[1]})

		# connection.close()

		# return {'items': items}