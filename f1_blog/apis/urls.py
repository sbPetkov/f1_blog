from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('merchandise/<str:category_name>/', views.MerchandiseListView.as_view(), name='merchandise-list'),
    path('merchandise/detail/<int:pk>/', views.MerchandiseDetailView.as_view(), name='merchandise-detail'),
]