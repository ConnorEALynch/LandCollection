from django.shortcuts import render
from django.http import HttpResponseNotFound,HttpResponseRedirect
from django.urls import reverse
from .models import card
from django.utils.text import slugify

def index(request):
    land_list = card.objects.objects()
    if not land_list:
        return HttpResponseNotFound("no cards found")
    else:
        return render(request, "card.html", {"card_list":land_list})
    
def byId(request, card_id):
    try:
        land = card.objects.get(_id=card_id)
        return render(request, "card.html", {"card":land})
    except:
        return HttpResponseNotFound("no cards with id: " + card_id)
    

def bySet(request, set):
    land_list = card.objects(set=set)
    if not land_list:
        return HttpResponseNotFound("no cards in " + set)
    else:
        return render(request, "cardList.html", {"card_list":land_list})

def byCollectorNumber(request, set,collector_number):
    try:
        #multiple db queries learn how to pass page context 
        land = card.objects.get(set=set, collector_number=collector_number, lang='en')
        slug_name = slugify(land.name)
        url = reverse("bySlug", kwargs={ "set":set,"collector_number":collector_number, "card_slug":slug_name })
        return HttpResponseRedirect(url)
    except:
        return HttpResponseNotFound("no cards in " + set + " with collector number " + collector_number)

def bySlug(request, set,collector_number, card_slug):
    try:
        land = card.objects.get(set=set, collector_number=collector_number, lang='en')
        name_slug = slugify(land.name)
        if card_slug != name_slug:
            url = reverse("bySlug", kwargs={ "set":set,"collector_number":collector_number, "card_slug":name_slug })
            return HttpResponseRedirect(url)
        return render(request, "card.html", {"card":land})
    except:
        return HttpResponseNotFound("no cards in " + set + " with collector number " + collector_number)


#query params get
# queryparam = request.GET.get('q', '')  



