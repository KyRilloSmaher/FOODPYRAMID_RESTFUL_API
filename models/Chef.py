from mongoengine import Document, StringField

class Chef(Document):
    name = StringField(required=True, max_length=80)
    image = StringField()
    desc = StringField() 
    def json(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "desc": self.desc,
            "image": self.image
        }
