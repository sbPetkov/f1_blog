from django.urls import path

from f1_blog.news import views

urlpatterns = [
   path('', views.PostListView.as_view(), name='post-index'),
   path('add_post/', views.PostAddView.as_view(), name='add-post'),
   path('details/<int:pk>', views.PostDetailView.as_view(), name='post-details'),
   path('toggle-like/<int:comment_id>/', views.toggle_comment_like, name='toggle-like'),
   ]
