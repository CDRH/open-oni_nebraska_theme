from django.shortcuts import render
from django.template import RequestContext

def about(request):
    page_title = "About Nebraska Newspapers"
    return render(request, 'about.html', locals())

def access(request):
    page_title = "About Nebraska Newspapers"
    return render(request, 'custom/access.html', locals())

def adding(request):
    page_title = "About Nebraska Newspapers"
    return render(request, 'custom/adding.html', locals())

def contact(request):
    page_title = "About Nebraska Newspapers"
    return render(request, 'custom/contact.html', locals())

def nnp(request):
    page_title = "About Nebraska Newspapers"
    return render(request, 'custom/nnp.html', locals())

def ndnp(request):
    page_title = "About Nebraska Newspapers"
    return render(request, 'custom/ndnp.html', locals())

def publishing(request):
    page_title = "Publishing History"
    return render(request, 'custom/publishing.html', locals())

