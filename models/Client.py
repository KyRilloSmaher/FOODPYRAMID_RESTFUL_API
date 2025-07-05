from mongoengine import (
    Document, StringField, ListField, ReferenceField,
    EmailField, ValidationError
)
from models.Dish import Dish
import re
class Client(Document):
    name = StringField(required=True, max_length=80)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True, min_length=8)
    phone = StringField()
    image = StringField()
    favorites = ListField(ReferenceField("Dish"))

    def clean(self):
        # Custom password validation
        if self.password:
            if len(self.password) < 8:
                raise ValidationError("Password must be at least 8 characters long.")
            if not re.search(r"[A-Z]", self.password):
                raise ValidationError("Password must contain at least one uppercase letter.")
            if not re.search(r"[a-z]", self.password):
                raise ValidationError("Password must contain at least one lowercase letter.")
            if not re.search(r"\d", self.password):
                raise ValidationError("Password must contain at least one digit.")
            if not re.search(r"[!@#$%^&*()_+=\-{}\[\]:;\"'<>,.?/~`]", self.password):
                raise ValidationError("Password must contain at least one special character.")

    def json(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "image": self.image,
            "favorites": [dish.json() for dish in self.favorites]
        }
