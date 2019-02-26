from django.conf.urls import url, include
from themes.nebraska import views

urlpatterns = [
  # about subpages
  url('access', views.access, name="nebraska_about_access"),
  url('adding', views.adding, name="nebraska_about_adding"),
  url('contact', views.contact, name="nebraska_about_contact"),
  url('nnp', views.nnp, name="nebraska_about_nnp"),

  # publishing history
  url('publishing', views.publishing, name="nebraska_publishing"),
]
