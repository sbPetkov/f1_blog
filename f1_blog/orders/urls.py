from django.urls import path
from .views import order_create_view, OrderListView, OrderDetailsView

urlpatterns = [
    path('submit/', order_create_view, name='order_submit'),
    path('order-lsit/', OrderListView.as_view(), name='order-list'),
    path('order-details/<int:pk>', OrderDetailsView.as_view(), name='review_order'),

]
