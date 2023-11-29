from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # ex: /card/id/123-12345345-3244354
    path("id/<str:card_id>", views.byId, name="byId"),
    # ex: /card/zen
    path("<str:set>", views.bySet, name="bySet"),
    # ex: /card/zen/223
    path("<str:set>/<str:collector_number>", views.byCollectorNumber, name="byCollectorNumber"),
    # ex: /card/zen/223/sclading-tarn
    path("<str:set>/<str:collector_number>/<slug:card_slug>", views.bySlug, name="bySlug")
]