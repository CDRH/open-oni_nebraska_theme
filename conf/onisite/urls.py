from django.urls import include, path, re_path
from onisite.plugins.featured_content import views as fc_views

urlpatterns = [
  # Plugin URLs
  re_path(r'', include("onisite.plugins.calendar.urls")),
  re_path(r'^$', fc_views.featured, name="featured_home"),
  re_path(r'^map', include("onisite.plugins.map.urls")),

  # Theme URLs
  path('', include("themes.nebraska.urls")),

  # Open ONI URLs
  path('', include("core.urls")),
]
