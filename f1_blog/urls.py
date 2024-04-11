from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('f1_blog.web.urls')),
    path('news/', include('f1_blog.news.urls')),
    path('videos/', include('f1_blog.videos.urls')),
    path('standings/', include('f1_blog.standings.urls')),
    path('merchandise/', include('f1_blog.merchandise.urls')),
    path('api/', include('f1_blog.apis.urls')),
    path('cart/', include('f1_blog.cart.urls')),
    path('orders/', include('f1_blog.orders.urls')),


]
