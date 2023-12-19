from mongoengine import *

class land(EmbeddedDocument):
    #do I need Id here?
    #id = StringField()
    card_id = StringField()
    foil = StringField()
    quality = StringField()
    donor = StringField()
    status = StringField()
    image_uris = DictField()

class binderEntry(Document):
    _id = ObjectIdField()
    name = StringField()
    oracle_id = StringField()
    oracle_text = StringField()
    type_line = StringField()
    release_date = StringField()
    default_image_uris = DictField()
    copies = EmbeddedDocumentListField(land)
    colours = ListField(StringField())
    binder = StringField()
    row = IntField()
    page = IntField()
    volume = IntField()
    order = IntField()
    meta = {
            'collection': 'Binders',
            'indexes': [
        {'fields': ['$name'],
         'default_language': 'english',
         'weights': {'name': 10}
        }
    ]}

class binderInfo(DynamicDocument):
    _id = ObjectIdField()
    name = StringField()
    pages = IntField()
    items_per_page = IntField()
    order = IntField()
    playset = IntField()
    sort = ListField()
    meta = {'collection': 'BinderInfo'}

   # def convertSort():



