from flask_restful import Resource

from models.Dish import Dish
from models.Client import Client


class ClientFavoritesResource(Resource):
    def post(self, client_id, dish_id):
        client = Client.objects(id=client_id).first()
        dish = Dish.objects(id=dish_id).first()

        if not client:
            return {"message": "Client not found"}, 404
        if not dish:
            return {"message": "Dish not found"}, 404

        if dish in client.favorites:
            return {"message": "Dish already in favorites"}, 400

        client.favorites.append(dish)
        client.save()
        return {"message": "Dish added to favorites", "favorites": [d.json() for d in client.favorites]}, 200
    def get(self, client_id,dish_id=None):
        client = Client.objects(id=client_id).first()
        if not client:
            return {"message": "Client not found"}, 404

        return {"favorites": [d.json() for d in client.favorites]}, 200
    def delete(self, client_id, dish_id):
        client = Client.objects(id=client_id).first()
        dish = Dish.objects(id=dish_id).first()

        if not client:
            return {"message": "Client not found"}, 404
        if not dish:
            return {"message": "Dish not found"}, 404

        if dish not in client.favorites:
            return {"message": "Dish not in favorites"}, 400

        client.favorites.remove(dish)
        client.save()
        return {"message": "Dish removed from favorites", "favorites": [d.json() for d in client.favorites]}, 200
