from django.urls import include, path, re_path
from themes.nebraska import views

urlpatterns = [
  # about subpages
  path('access', views.access, name="nebraska_about_access"),
  path('adding', views.adding, name="nebraska_about_adding"),
  path('contact', views.contact, name="nebraska_about_contact"),
  path('nnp', views.nnp, name="nebraska_about_nnp"),

  # publishing history
  path('publishing', views.publishing, name="nebraska_publishing"),
]
