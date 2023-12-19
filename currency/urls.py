from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('countries/', views.countries_view, name='countries'),
    path('about/', views.about_view, name='about')
]
