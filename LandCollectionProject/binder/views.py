from django.shortcuts import render
from django.http import *
from .models import *
from .card_paginator import CardPaginator




info = binderInfo.objects()

#array of array of binders
def index(request):
    #nested loop is awful upadtae to be more async implementing jquery
    results =[]
    for binder in info:
        i = 1
        binders = []
        moreVolumes = True
        while moreVolumes:

            kwargs =  {"binder": binder.name, "volume": i, "page":1}
            if binder.sort[0] == "name":
                kwargs = {"binder": binder.name, "volume": i}
            volume = binderEntry.objects(**kwargs).order_by('volume', 'page', 'row')
            if len(volume) == 0:
                moreVolumes = False
                break
            paginator = CardPaginator(volume, binder,binder.name,1)

            binders.append( paginator.get_page(1))
            i += 1
        results.append(binders)

    return render(request, "index.html",  {"items": results})
    
    #array of binders
def byBinder(request, binder_name):
    try:
        binderSpecs = info.get(name=binder_name)
    except :
        return HttpResponseNotFound(f"No binder with name:{binder_name} ")
    i = 1
    binders = []
    moreVolumes = True
    while moreVolumes:

        kwargs =  {"binder": binder_name, "volume": i, "page":1}
        if binderSpecs.sort[0] == "name":
            kwargs = {"binder": binder_name, "volume": i}
        volume = binderEntry.objects(**kwargs).order_by('volume', 'page', 'row')
        if len(volume) == 0:
            moreVolumes = False
            break
        paginator = CardPaginator(volume, binderSpecs,binder_name,1)

        binders.append( paginator.get_page(1))
        i += 1

    return render(request, "binders.html",  {"binders": binders})


#binder view
def byVolume(request,binder_name, volume_number):
    
    try:
        binderSpecs = info.get(name=binder_name)
    except :
        return HttpResponseNotFound(f"No binder with name:{binder_name} ")
    kwargs =  {"binder": binder_name, "volume": volume_number, "page":1}
    if binderSpecs.sort[0] == "name":
        kwargs = {"binder": binder_name, "volume": volume_number}
    volume = binderEntry.objects(**kwargs).order_by('volume', 'page', 'row')
    paginator = CardPaginator(volume, binderSpecs,binder_name,volume_number)

    return render(request, "volume.html", {"context": paginator.get_page(1)})

#page view
def byPage(request, binder_name, volume_number, page_number):
    embedded = request.GET.get('embedded', '')  
    try:
        binderSpecs = info.get(name=binder_name)
    except :
        return HttpResponseNotFound(f"No binder with name:{binder_name} ")
    kwargs =  {"binder": binder_name, "volume": volume_number, "page":page_number}
    if binderSpecs.sort[0] == "name":
        kwargs = {"binder": binder_name, "volume": volume_number}

    page = binderEntry.objects(**kwargs).order_by('volume', 'page', 'row')
    paginator = CardPaginator(page, binderSpecs, binder_name, volume_number)
    test = paginator.get_page(page_number)
    result = render(request, "page.html", {"context": test })
    if embedded == "True":
        result = render(request, "pageEmbed.html", {"context": test })
    return result


#row view
def byRow(request,binder_name,volume_number, page_number, row_number):
    try:
        binderSpecs = info.get(name=binder_name)
    except :
         return HttpResponseNotFound(f"No binder with name:{binder_name} ")
    row = binderEntry.objects().get(binder=binder_name, volume=volume_number, page=page_number,row=row_number) #.order_by('volume', 'page', 'row')
    return render(request, "row.html", {"row":row})

#row view
def byid(request,binder_name, card_id):
    try:
        binderSpecs = info.get(name=binder_name)
    except :
         return HttpResponseNotFound(f"No binder with name:{binder_name} ")
    entry_list = binderEntry.objects(binder=binder_name, oracle_id=card_id)
    return render(request, "row.html", {"row":entry_list})
#implement later
def byColour(request,binder_name, card_id):
    card = binderEntry.objects.get(binder=binder_name,oracle_id=card_id) 
    return render(request, "row.html", {"binder_entry":card})


#turn into decorator
def verifyRequest(request, binder_name, volume_number=None, page_number=None, row_number=None):

    try:
        binderStat = info.get(name=binder_name)
    except: 
        HttpResponseNotFound(f"No binder with name:{binder_name} ")

    if binderStat.pages and page_number > binderStat.pages :
        HttpResponseNotFound(f"page number of {binder_name} exceds item binder max of {binderStat.pages}")

    if binderStat.items_per_page and row_number > binderStat.items_per_page:
         HttpResponseNotFound(f"row number of {binder_name} exceds page max of {binderStat.items_per_page}")




