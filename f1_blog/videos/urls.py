from django.urls import path
from . import views

urlpatterns = [
   path('', views.VideoListView.as_view(), name='video-index'),
   path('add/', views.AddVideoView.as_view(), name='video-add'),
   path('details/<int:pk>', views.VideoDetailView.as_view(), name='video-details'),
   path('video/<int:pk>/comment/', views.VideoDetailView.as_view(), name='add_comment'),
   ]
