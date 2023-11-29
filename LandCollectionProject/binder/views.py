from django.shortcuts import render
from django.http import *
from .models import *
from .bindernator import *


info = binderInfo.objects()

#array of array of binders
def index(request):
    #all_entries = binderEntry.objects()
    collections = []
    for item in info:
        collections.append( binderEntry.objects(binder=item.name).order_by(*item.sort))

    return render(request, "index.html", {"context":collections})
    
    #array of binders
def byBinder(request, binder_name):
    try:
        binderSpecs = info.get(name=binder_name)
    except :
        return HttpResponseNotFound(f"No binder with name:{binder_name} ")
    
    binders = binderEntry.objects(binder=binder_name).order_by(*binderSpecs.sort)
    return render(request, "binders.html", {"binders":binders})


#binder view
def byVolume(request,binder_name, volume):
    
    try:
        binderSpecs = info.get(name=binder_name)
    except :
        return HttpResponseNotFound(f"No binder with name:{binder_name} ")
    entry_list = binderEntry.objects(binder=binder_name).order_by(*binderSpecs.sort)
    return render(request, "volume.html", {"binder":entry_list})

#page view
def byPage(request, binder_name, volume, page_number):

    try:
        binderSpecs = info.get(name=binder_name)
    except :
        return HttpResponseNotFound(f"No binder with name:{binder_name} ")
    entry_list = binderEntry.objects(binder=binder_name).order_by(*binderSpecs.sort)
    return render(request, "page.html", {"page_obj":entry_list})


#row view
def byRow(request,binder_name,volume, page_number, row_number):
    try:
        binderSpecs = info.get(name=binder_name)
    except :
         return HttpResponseNotFound(f"No binder with name:{binder_name} ")
    entry_list = binderEntry.objects(binder=binder_name).order_by(*binderSpecs.sort)
    return render(request, "row.html", {"row_obj":entry_list})

#row view
def byid(request,binder_name, card_id):
    try:
        binderSpecs = info.get(name=binder_name)
    except :
         return HttpResponseNotFound(f"No binder with name:{binder_name} ")
    entry_list = binderEntry.objects(binder=binder_name, oracle_id=card_id)
    return render(request, "row.html", {"row_obj":entry_list})
#implement later
def byColour(request,binder_name, card_id):
    card = binderEntry.objects.get(binder=binder_name,oracle_id=card_id) 
    return render(request, "row.html", {"binder_entry":card})



