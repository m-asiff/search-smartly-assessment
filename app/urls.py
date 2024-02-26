from django.urls import path
from . import views

urlpatterns = [path("", views.poi_list_view, name="poi_list_view")]
