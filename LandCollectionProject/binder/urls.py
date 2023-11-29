from django.urls import path
from . import views


urlpatterns = [
    #ex: /binder
    path("", views.index, name="index"),
    # ex: /binder/Monocolour
    path("<str:binder_name>", views.byBinder, name="byBinder"),
    
    
    # ex: /binder/Monocolour/volume/1
    #path("<str:binder_name>/volume/<int:volume>", views.byVolume, name="byVolume"),
    # ex: /binder/Monocolour/volume/page/5
    #path("<str:binder_name>/volume/<int:volume>/page/<int:page_number>", views.byPage, name="byPage"),
    # ex: /binder/Monocolour/volume/1/page/5/2
    #path("<str:binder_name>/volume/<int:volume>/page/<int:page_number>/<int:row_number>", views.byRow, name="byRow"),
    # ex: /binder/Monocolour/volume/1/page/5/row/2
    #path("<str:binder_name>/volume/<int:volume>/page/<int:page_number>/row/<int:row_number>", views.byRow, name="byRow"),
    # ex: /binder/Monocolour/colours/U
    #path("<str:binder_name>/colours/<str:colour>", views.byColour, name="byColour"),

]