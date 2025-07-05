from flask import Flask, send_from_directory
from flask_cors import CORS 
from flask_restful import Api
from db import init_db
from resources.ClientFavoritesResource import ClientFavoritesResource
from resources.Chef import ChefResource
from resources.Kitchen import KitchenResource
from resources.Dish import DishResource
from resources.KitchenDishesResource import KitchenDishesResource
from resources.Client import ClientResource

app = Flask(__name__)
api = Api(app)


# Connect MongoEngine directly here
init_db() 

# Configuration for file uploads

app.config['UPLOAD_FOLDER'] = 'static/images'


# Routes
api.add_resource(ChefResource,'/chefs', '/chefs/<string:chef_id>')
api.add_resource(KitchenResource,'/kitchens', '/kitchens/<string:kitchen_id>')
api.add_resource(DishResource,'/dishes', '/dishes/<string:dish_id>')
api.add_resource(ClientResource, "/clients", "/clients/<string:client_id>")
api.add_resource(ClientFavoritesResource,"/clients/<string:client_id>/favorites/<string:dish_id>","/clients/<string:client_id>/favorites/")
api.add_resource(KitchenDishesResource, '/kitchens/<string:kitchen_id>/dishes')

#Run the Flask application
CORS(app)
if __name__ == '__main__':
    app.run(debug=True)
