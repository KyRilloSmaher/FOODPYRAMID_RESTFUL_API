import os
import re
from bson import ObjectId
from flask import request, current_app
from flask_restful import Resource, reqparse
from werkzeug.utils import secure_filename
from mongoengine import ValidationError
from models import Dish
from models.Client import Client

# Configuration
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_IMAGE_SIZE = 2 * 1024 * 1024  # 2MB

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True)
parser.add_argument('email', type=str, required=True)
parser.add_argument('phone', type=str)
parser.add_argument('password', type=str, required=True)
parser.add_argument('image', type=str)
parser.add_argument('favorites', type=str, action='append')  # List of dish IDs

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_strong_password(password):
    return (
        len(password) >= 8 and
        re.search(r"[A-Z]", password) and
        re.search(r"[a-z]", password) and
        re.search(r"\d", password)
    )

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class ClientResource(Resource):
    def get(self, client_id=None):
        print(client_id)
        if client_id:
            try:
                client = Client.objects.get(id=ObjectId(client_id))
                return client.json(), 200
            except (Client.DoesNotExist, ValidationError):
                return {"message": "Client not found"}, 404
            
        email = request.args.get("email")
        password = request.args.get("password")
        
        if email and password:
            client = Client.objects(email=email, password=password).first()
            return client.json() if client else {"message": "Client not found"}

        return [client.json() for client in Client.objects()], 200

    def post(self):
        # Handle form data
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')
        
        # Handle file upload
        image_file = request.files.get('image')
        image_url = None
        if image_file and allowed_file(image_file.filename) and image_file.tell() <= MAX_IMAGE_SIZE:
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
            image_url = f"/static/images/{filename}"

        # Email validation
        if not is_valid_email(email):
            return {"message": "Invalid email format."}, 400

        if not is_strong_password(password):
            return {"message": "Password must be at least 8 characters with uppercase, lowercase, and numbers."}, 400

        if Client.objects(email=email).first():
            return {"message": "Email already registered."}, 400

        try:
            client = Client(
                name=name,
                email=email,
                password=password,
                phone=phone,
                image=image_url,
                favorites=[]  # Initialize with empty favorites
            )
            client.save()
            return client.json(), 201
        except ValidationError as e:
            return {"message": str(e)}, 400

    def put(self, client_id):
        data = parser.parse_args()
        
        try:
            client = Client.objects.get(id=ObjectId(client_id))
        except (Client.DoesNotExist, ValidationError):
            return {"message": "Client not found"}, 404

        # Handle image update if new image is provided
        image_file = request.files.get('image')
        image_url = client.image  # Keep existing if no new image
        
        if image_file:
            if not allowed_file(image_file.filename):
                return {"message": f"Invalid image format. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"}, 400

            image_file.seek(0, os.SEEK_END)
            size = image_file.tell()
            image_file.seek(0)
            if size > MAX_IMAGE_SIZE:
                return {"message": "Image file too large. Max size: 2MB."}, 400

            filename = secure_filename(image_file.filename)
            upload_folder = current_app.config.get('UPLOAD_FOLDER', 'static/images')
            os.makedirs(upload_folder, exist_ok=True)
            image_path = os.path.join(upload_folder, filename)
            image_file.save(image_path)
            image_url = f"/static/images/{filename}"

        # Handle favorites update
        favorite_dishes = []
        if data['favorites']:
            for fid in data['favorites']:
                try:
                    dish = Dish.objects.get(id=ObjectId(fid))
                    favorite_dishes.append(dish)
                except (Dish.DoesNotExist, ValidationError):
                    continue

        try:
            client.update(
                name=data['name'],
                email=data['email'],
                password=data['password'],
                phone=data.get('phone'),
                image=image_url,
                favorites=favorite_dishes
            )
            client.reload()  # Refresh the document from DB
            return client.json(), 200
        except ValidationError as e:
            return {"message": str(e)}, 400

    def delete(self, client_id):
        try:
            client = Client.objects.get(id=ObjectId(client_id))
            client.delete()
            return {"message": "Client deleted successfully"}, 200
        except (Client.DoesNotExist, ValidationError):
            return {"message": "Client not found"}, 404