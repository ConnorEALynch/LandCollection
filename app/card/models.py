from mongoengine import *


class card(DynamicDocument):
    _id = StringField()
    object = StringField()
    oracle_id = StringField()
    multiverse_ids = ListField(IntField())
    mtgo_id = IntField()
    mtgo_foil_id = IntField()
    tcgplayer_id = IntField()
    cardmarket_id = IntField()
    name = StringField()
    lang = StringField()
    released_at = StringField()
    #update this to be date
    uri = StringField()
    scryfall_uri = StringField()
    layout = StringField()
    highres_image = BooleanField()
    image_status = StringField()
    image_uris = DictField()
    mana_cost = StringField()
    cmc = FloatField()
    #this field is kinda useless except for mdfc
    type_line = StringField()
    oracle_text = StringField()
    colors = ListField(StringField())
    color_identity = ListField(StringField())
    keywords = ListField()
    produced_mana = ListField(StringField())
    all_parts = ListField(DictField())
    legalities = DictField()
    games = ListField()
    reserved = BooleanField()
    foil = BooleanField()
    nonfoil = BooleanField()
    finishes = ListField(StringField())
    oversized = BooleanField()
    promo = BooleanField()
    reprint = BooleanField()
    variation = BooleanField()
    set_id = StringField()
    set = StringField()
    set_name = StringField()
    set_type = StringField()
    set_uri = StringField()
    set_search_uri = StringField()
    scryfall_set_uri = StringField()
    rulings_uri = StringField()
    prints_search_uri = StringField()
    collector_number = StringField()
    digital = BooleanField()
    rarity = StringField()
    card_back_id = StringField()
    artist = StringField()
    artist_ids = ListField(StringField())
    illustration_id = StringField()
    border_color = StringField()
    frame = StringField()
    security_stamp = StringField()
    full_art = BooleanField()
    textless = BooleanField()
    booster = BooleanField()
    story_spotlight = BooleanField()
    edhrec_rank = IntField()
    penny_rank = IntField()
    prices = DictField()
    related_uris = DictField()
    purchase_uris = DictField()
    binder = StringField()
    binder_id = ObjectIdField()
    meta = {'collection': 'Lands'}