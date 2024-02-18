from mongoengine import *

class land(EmbeddedDocument):
    card_id = StringField()
    foil = StringField()
    quality = StringField()
    donor = StringField()
    status = StringField()
    border_color = StringField()
    set = StringField()
    image_uris = DictField()
    card_faces = GenericEmbeddedDocumentField()

class default(EmbeddedDocument):
    card_id = StringField()
    border_color = StringField()
    set = StringField()
    image_uris = DictField()
    card_faces = GenericEmbeddedDocumentField()

class binderEntry(Document):
    _id = ObjectIdField()
    name = StringField()
    oracle_id = StringField()
    oracle_text = StringField()
    type_line = StringField()
    released_at = StringField()
    copies = EmbeddedDocumentListField(land)
    colours = ListField(StringField())
    binder = StringField()
    row = IntField()
    page = IntField()
    volume = IntField()
    order = IntField()
    reserved = BooleanField()
    power = IntField()
    toughness = IntField()
    default = EmbeddedDocumentField(default)
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



