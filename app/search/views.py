from django.shortcuts import render
from binder.models import binderEntry
from django.http import HttpResponseNotFound,HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import *




def homepage(request):

    return render(request,"homepage.html")

def random(request):
    results = binderEntry.objects().aggregate([{'$sample': {'size': 1}}])
    for land in results:
        reverseURL = "byPage"
        kwargs = {"binder_name":land["binder"], "volume_number":land["volume"], "page_number":land["page"] }

        if land["binder"] !="CommonUncommon":
            reverseURL = "byRow"
            kwargs["row_number"] = land["row"]

        url = reverse(reverseURL, kwargs=kwargs )
        return HttpResponseRedirect(url)
    

def index(request):
    #expnad to use more fields later
    name_param = request.GET.get('name', '')
    page_param = request.GET.get('page', 1)

    #implement a regex later. implement Atlas search index when supported later later
    entry_list = binderEntry.objects.search_text(name_param).order_by('binder','volume','page','row')
    if len(entry_list) == 1 :
        land  = entry_list[0]
        if (land.binder == "CommonUncommon"):
            url = reverse("byPage", kwargs={ "binder_name":land.binder,"volume_number":land.volume, "page_number":land.page})
        else:
            url = reverse("byRow", kwargs={ "binder_name":land.binder,"volume_number":land.volume, "page_number":land.page, "row_number":land.row})

        return HttpResponseRedirect(url)
    paginator = Paginator(entry_list, 10)
    search_page = paginator.get_page(page_param)
    result = render(request, "multiItem.html", {"context":search_page})
    return result 
