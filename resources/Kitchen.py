from flask_restful import Resource, reqparse

from models.Chef import Chef
from models.Kitchen import Kitchen




parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True)
parser.add_argument('image', type=str)
parser.add_argument('desc', type=str)
parser.add_argument('headchef_id', type=str, required=True)

class KitchenResource(Resource):
    def get(self, kitchen_id=None):
        if kitchen_id:
            k = Kitchen.objects(id=kitchen_id).first()
            return k.json() if k else {"message": "Kitchen not found"}, 404
        return [k.json() for k in Kitchen.objects()]

    def post(self):
        data = parser.parse_args()
        chef = Chef.objects(id=data['headchef_id']).first()
        if not chef:
            return {"message": "Chef not found"}, 404
        kitchen = Kitchen(name=data['name'], image=data.get('image'), desc = data.get('desc'),headchef=chef).save()
        return kitchen.json(), 201

    def put(self, kitchen_id):
        data = parser.parse_args()
        kitchen = Kitchen.objects(id=kitchen_id).first()
        if not kitchen:
            return {"message": "Kitchen not found"}, 404
        chef = Chef.objects(id=data['headchef_id']).first()
        if not chef:
            return {"message": "Chef not found"}, 404
        kitchen.update(name=data['name'], image=data.get('image'),  desc = data.get('desc'),headchef=chef)
        return Kitchen.objects(id=kitchen_id).first().json()

    def delete(self, kitchen_id):
        kitchen = Kitchen.objects(id=kitchen_id).first()
        if not kitchen:
            return {"message": "Kitchen not found"}, 404
        kitchen.delete()
        return {"message": "Kitchen deleted"}