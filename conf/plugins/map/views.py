from django.shortcuts import render
from django.template import RequestContext

from core.models import Place

def map(request):
    places = Place.objects.filter(titles__has_issues=1).order_by("city").distinct()

    # NE theme change
    page_title = "Map of Cities"
    # / NE theme change
    return render(request, 'map.html', locals())
