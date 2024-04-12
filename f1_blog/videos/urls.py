from django.urls import path
from . import views

urlpatterns = [
    path('', views.VideoListView.as_view(), name='video-index'),
    path('add/', views.AddVideoView.as_view(), name='video-add'),
    path('details/<int:pk>', views.VideoDetailView.as_view(), name='video-details'),
    path('<int:pk>/comment/', views.VideoDetailView.as_view(), name='add_comment'),
    path('edit/<int:pk>/', views.VideoEditView.as_view(), name='video-edit'),
    path('delete/<int:pk>/', views.VideoDeleteView.as_view(), name='video-delete'),
]
