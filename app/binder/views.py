from django.shortcuts import render
from django.urls import reverse
from django.http import *
from .models import *
from .card_paginator import CardPaginator




info = binderInfo.objects()

#array of array of binders
def index(request):
    #nested loop is awful upadtae to be more async implementing jquery
    #results =[]
    # for binder in info:
        # i = 1
        # binders = []
        # moreVolumes = True
        # while moreVolumes:

        #     kwargs =  {"binder": binder.name, "volume": i, "page":1}
        #     if binder.sort[0] == "name":
        #         kwargs = {"binder": binder.name, "volume": i}
        #     volume = binderEntry.objects(**kwargs).order_by('volume', 'page', 'row')
        #     if len(volume) == 0:
        #         moreVolumes = False
        #         break
        #     paginator = CardPaginator(volume, binder,binder.name,1)

        #     binders.append( paginator.get_page(1))
        #     i += 1
        # results.append(binders)

    return render(request, "index.html",  {"context":info})
    
    #array of binders
def byBinder(request, binder_name):
    try:
        binderSpecs = info.get(name=binder_name)
    except :
        return HttpResponseNotFound(f"No binder with name:{binder_name} ")
    
    entry = binderEntry.objects(binder=binder_name).order_by('-volume')[:1]
    if len(entry) > 0:
        max = entry[0]
    else:
         return HttpResponseServerError()
    # i = 1
    # binders = []
    # moreVolumes = True
    # while moreVolumes:

    #     kwargs =  {"binder": binder_name, "volume": i, "page":1}
    #     if binderSpecs.sort[0] == "name":
    #         kwargs = {"binder": binder_name, "volume": i}
    #     volume = binderEntry.objects(**kwargs).order_by('volume', 'page', 'row')
    #     if len(volume) == 0:
    #         moreVolumes = False
    #         break
    #     paginator = CardPaginator(volume, binderSpecs,binder_name,1)

    #     binders.append( paginator.get_page(1))
    #     i += 1

#temporary and terible
    return render(request, "binders.html",  {"context": {"volumes":range(max.volume), "binder":binder_name}})


#binder view
def byVolume(request,binder_name, volume_number):
    url = reverse("byPage", kwargs={"binder_name":binder_name, "volume_number":volume_number, "page_number":1 })
    return HttpResponseRedirect(url)

#page view
def byPage(request, binder_name, volume_number, page_number):
    format = request.GET.get('format', '')  
    try:
        binderSpecs = info.get(name=binder_name)
    except :
        return HttpResponseNotFound(f"No binder with name:{binder_name} ")
    
    result = HttpResponseServerError()
    if binderSpecs.sort[0] == "name":
        template = "item.html"
        row = binderEntry.objects(binder=binder_name, volume=volume_number).order_by('volume', 'page', 'row')
        paginator = CardPaginator(row, binderSpecs, binder_name, volume_number)
        binder_page = paginator.get_page(page_number)
        result = render(request, "CUhotfix.html", {"context":binder_page})
        if format == "json":
            result =JsonResponse(binder_page)

    else:
        page = binderEntry.objects(binder=binder_name,volume=volume_number,page=page_number).order_by('volume', 'page', 'row')
        paginator = CardPaginator(page, binderSpecs, binder_name, volume_number)
        binder_page = paginator.get_page(page_number)
        result = render(request, "multiItem.html", {"context": binder_page })
        if format == "json":
            result =JsonResponse(binder_page)

    return result


#row view
def byRow(request,binder_name,volume_number, page_number, row_number):
    try:
        binderSpecs = info.get(name=binder_name)
    except :
         return HttpResponseNotFound(f"No binder with name:{binder_name} ")
    row = binderEntry.objects().get(binder=binder_name, volume=volume_number, page=page_number,row=row_number) #.order_by('volume', 'page', 'row')
    return render(request, "item.html", {"context":row})

#row view
def byid(request,card_id):

    format = request.GET.get('format', '')  
    card = binderEntry.objects.get(oracle_id=card_id)
    result = render(request, "item.html", {"context": card })
    if format == "json":
        jsonobj = card.to_json()
        result =JsonResponse(jsonobj, safe=False)
    return result


#implement later
def byColour(request,binder_name, card_id):
    card = binderEntry.objects.get(binder=binder_name,oracle_id=card_id) 
    return render(request, "item.html", {"context":card})


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




