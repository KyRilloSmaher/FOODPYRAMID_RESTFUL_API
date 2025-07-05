
from mongoengine import Document, StringField, ReferenceField, CASCADE
from models.Chef import Chef
class Kitchen(Document):
    name = StringField(required=True, max_length=80)
    image = StringField()
    desc = StringField()
    headchef = ReferenceField("Chef", required=True, reverse_delete_rule=CASCADE)
 

    @classmethod
    def find_by_name(cls, name):
        return cls.objects(name=name).first()

    def save_to_db(self):
        self.save()

    def delete_from_db(self):
        self.delete()

    def json(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "desc": self.desc,
            "image": self.image,
            "headchef": self.headchef.json() if self.headchef else None
        }