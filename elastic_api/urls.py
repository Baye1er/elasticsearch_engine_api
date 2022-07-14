from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('engine/', views.PublisherDocumentView.as_view({'get': 'list'})),
]