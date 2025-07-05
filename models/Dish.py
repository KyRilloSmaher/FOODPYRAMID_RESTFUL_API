from mongoengine import Document, StringField, FloatField, ReferenceField, CASCADE
from models.Kitchen import Kitchen  
class Dish(Document):
    name = StringField(required=True, max_length=80)
    price = FloatField(required=True, precision=2)
    image = StringField()
    desc = StringField()
    kitchen = ReferenceField("Kitchen", required=True, reverse_delete_rule=CASCADE)  

    def json(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "price": self.price,
            "desc": self.desc,
            "image": self.image,
            "kitchen": self.kitchen.json() if self.kitchen else None
        }
