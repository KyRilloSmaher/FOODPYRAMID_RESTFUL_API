# --- /resources/dish_resource.py ---
from flask_restful import Resource, reqparse

from models import Dish
from models.Kitchen import Kitchen


parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True)
parser.add_argument('price', type=float, required=True)
parser.add_argument('image', type=str)
parser.add_argument('kitchen_id', type=str, required=True)

class DishResource(Resource):
    def get(self, dish_id=None):
        if dish_id:
            d = Dish.objects(id=dish_id).first()
            return d.json() if d else {"message": "Dish not found"}, 404
        return [d.json() for d in Dish.objects()]
    def post(self):
        data = parser.parse_args()
        kitchen = Kitchen.objects(id=data['kitchen_id']).first()
        if not kitchen:
            return {"message": "Kitchen not found"}, 404
        dish = Dish(name=data['name'], price=data['price'], image=data.get('image'),  desc = data.get('desc'),kitchen=kitchen).save()
        return dish.json(), 201

    def put(self, dish_id):
        data = parser.parse_args()
        dish = Dish.objects(id=dish_id).first()
        if not dish:
            return {"message": "Dish not found"}, 404
        kitchen = Kitchen.objects(id=data['kitchen_id']).first()
        if not kitchen:
            return {"message": "Kitchen not found"}, 404
        dish.update(name=data['name'], price=data['price'], image=data.get('image'),  desc = data.get('desc'),kitchen=kitchen)
        return Dish.objects(id=dish_id).first().json()

    def delete(self, dish_id):
        dish = Dish.objects(id=dish_id).first()
        if not dish:
            return {"message": "Dish not found"}, 404
        dish.delete()
        return {"message": "Dish deleted"}
