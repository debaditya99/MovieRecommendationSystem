from django.urls import path
from . import views

urlpatterns = [
    #path('movie/', views.movie, name='movie'),
    path('result/', views.result, name='result'),
    path('movie/', views.movie, name='movie')
]
