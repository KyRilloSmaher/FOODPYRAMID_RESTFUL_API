
from flask_restful import Resource, reqparse

from models.Chef import Chef


parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True)
parser.add_argument('image', type=str)
parser.add_argument('desc', type=str)

class ChefResource(Resource):
    def get(self, chef_id=None):
        if chef_id:
            chef = Chef.objects(id=chef_id).first()
            return chef.json() if chef else {"message": "Chef not found"}, 404
        return [chef.json() for chef in Chef.objects()]

    def post(self):
        data = parser.parse_args()
        chef = Chef(name=data['name'],  desc = data.get('desc') ,image=data.get('image')).save()
        return chef.json(), 201

    def put(self, chef_id):
        data = parser.parse_args()
        chef = Chef.objects(id=chef_id).first()
        if not chef:
            return {"message": "Chef not found"}, 404
        chef.update(name=data['name'],  desc = data.get('desc'),image=data.get('image'))
        return Chef.objects(id=chef_id).first().json()

    def delete(self, chef_id):
        chef = Chef.objects(id=chef_id).first()
        if not chef:
            return {"message": "Chef not found"}, 404
        chef.delete()
        return {"message": "Chef deleted"}