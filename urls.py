from django.conf.urls import url, include
from themes.nebraska import views

urlpatterns = [
  # publishing history
  url('publishing', views.publishing, name="nebraska_publishing"),
]
