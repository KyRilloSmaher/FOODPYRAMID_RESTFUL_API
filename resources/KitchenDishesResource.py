
from flask_restful import Resource

from models.Kitchen import Kitchen
from models.Dish import Dish


class KitchenDishesResource(Resource):
    def get(self, kitchen_id):
        kitchen = Kitchen.objects(id=kitchen_id).first()
        if not kitchen:
            return {"message": "Kitchen not found"}, 404
        dishes = Dish.objects(kitchen=kitchen)
        return [d.json() for d in dishes]