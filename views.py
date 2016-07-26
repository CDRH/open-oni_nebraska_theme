from django.shortcuts import render_to_response
from django.template import RequestContext

def publishing(request):
    page_title = "Publishing History"
    return render_to_response('custom/publishing.html', 
                            dictionary=locals(), 
                            context_instance=RequestContext(request))
