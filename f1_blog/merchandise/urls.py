from django.urls import path
from . import views

urlpatterns = [
    path('', views.MerchandiseView.as_view(), name='merchandise-list'),
]
