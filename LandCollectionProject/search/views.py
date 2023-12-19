from django.shortcuts import render
from binder.models import binderEntry
from django.http import HttpResponseNotFound,HttpResponseRedirect
from django.urls import reverse


def homepage(request):

    return render(request,"homepage.html")

def index(request):
    #expnad to use more fields later
    queryparam = request.GET.get('name', '') 
    #implement a regex later. implement Atlas search index when supported later later
    entry_list = binderEntry.objects.search_text(queryparam).order_by('binder','volume','page','row')
    if len(entry_list) == 1 :
        land  = entry_list[0]
        url = reverse("byOracleId", kwargs={ "oracle_id":land.oracle_id })
        return HttpResponseRedirect(url)
    result = render(request, "results.html", {"results":entry_list})
    return result 
