from django.shortcuts import render_to_response
from django.template import RequestContext

def about(request):
    page_title = "About Nebraska Newspapers"
    return render_to_response('about.html', 
                            dictionary=locals(), 
                            context_instance=RequestContext(request))

def access(request):
    page_title = "About Nebraska Newspapers"
    return render_to_response('custom/access.html', 
                            dictionary=locals(), 
                            context_instance=RequestContext(request))
def adding(request):
    page_title = "About Nebraska Newspapers"
    return render_to_response('custom/adding.html', 
                            dictionary=locals(), 
                            context_instance=RequestContext(request))

def contact(request):
    page_title = "About Nebraska Newspapers"
    return render_to_response('custom/contact.html', 
                            dictionary=locals(), 
                            context_instance=RequestContext(request))

def nnp(request):
    page_title = "About Nebraska Newspapers"
    return render_to_response('custom/nnp.html', 
                            dictionary=locals(), 
                            context_instance=RequestContext(request))

def ndnp(request):
    page_title = "About Nebraska Newspapers"
    return render_to_response('custom/ndnp.html', 
                            dictionary=locals(), 
                            context_instance=RequestContext(request))

def publishing(request):
    page_title = "Publishing History"
    return render_to_response('custom/publishing.html', 
                            dictionary=locals(), 
                            context_instance=RequestContext(request))


