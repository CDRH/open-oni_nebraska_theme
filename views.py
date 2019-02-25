from django.shortcuts import render
from django.template import RequestContext

def about(request):
    page_title = "About Nebraska Newspapers"
    return render(request, 'about.html', locals())

def publishing(request):
    page_title = "Publishing History"
    return render(request, 'custom/publishing.html', locals())

