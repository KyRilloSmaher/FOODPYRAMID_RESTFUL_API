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
                return {"message": "Client not found"}
            
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
        try:
            client = Client.objects.get(id=ObjectId(client_id))
        except (Client.DoesNotExist, ValidationError):
            return {"message": "Client not found"}, 404

        content_type = request.content_type or ""
        
        # Case 1: Multipart form — image and/or data update
        if "multipart/form-data" in content_type:
            form = request.form.to_dict()
            image_file = request.files.get('image')
            update_fields = {}

            # Image processing
            if image_file:
                if not allowed_file(image_file.filename):
                    return {"message": f"Invalid image format. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"}, 400
                image_file.seek(0, os.SEEK_END)
                size = image_file.tell()
                image_file.seek(0)
                if size > MAX_IMAGE_SIZE:
                    return {"message": "Image file too large. Max size: 2MB."}, 400
                filename = secure_filename(image_file.filename)
                path = os.path.join(current_app.config.get('UPLOAD_FOLDER', 'static/images'), filename)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                image_file.save(path)
                update_fields['image'] = f"/static/images/{filename}"

            # Optional data fields (name, email, phone, password)
            name = form.get('name')
            email = form.get('email')
            phone = form.get('phone')
            password = form.get('password')

            if email and email != client.email:
                if not is_valid_email(email):
                    return {"message": "Invalid email format."}, 400
                if Client.objects(email=email).first():
                    return {"message": "Email already registered."}, 400
                update_fields['email'] = email

            if name:
                update_fields['name'] = name
            if phone:
                update_fields['phone'] = phone
            if password and password != client.password:
                if not is_strong_password(password):
                    return {"message": "Weak password."}, 400
                update_fields['password'] = password

            if update_fields:
                client.update(**update_fields)
                client.reload()
                return {"message": "Client updated successfully", "client": client.json()}, 200
            return {"message": "No data provided to update"}, 400

        # Case 2: JSON only — data update (no image)
        elif "application/json" in content_type:
            data = request.get_json()
            update_fields = {}

            name = data.get('name')
            email = data.get('email')
            phone = data.get('phone')
            password = data.get('password')

            if email and email != client.email:
                if not is_valid_email(email):
                    return {"message": "Invalid email format."}, 400
                if Client.objects(email=email).first():
                    return {"message": "Email already registered."}, 400
                update_fields['email'] = email

            if name:
                update_fields['name'] = name
            if phone:
                update_fields['phone'] = phone
            if password and password != client.password:
                if not is_strong_password(password):
                    return {"message": "Weak password."}, 400
                update_fields['password'] = password

            if update_fields:
                client.update(**update_fields)
                client.reload()
                return {"message": "Client updated successfully", "client": client.json()}, 200
            return {"message": "No data provided to update"}, 400

        else:
            return {"message": "Unsupported Content-Type. Use 'multipart/form-data' or 'application/json'."}, 415


    def delete(self, client_id):
        try:
            client = Client.objects.get(id=ObjectId(client_id))
            client.delete()
            return {"message": "Client deleted successfully"}, 200
        except (Client.DoesNotExist, ValidationError):
            return {"message": "Client not found"}, 404