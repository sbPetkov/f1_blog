from rest_framework import generics
from .serializers import CategorySerializer, MerchandiseSerializer
from ..merchandise.models import Category, Merchandise


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MerchandiseListView(generics.ListAPIView):
    serializer_class = MerchandiseSerializer

    def get_queryset(self):
        category_name = self.kwargs.get('category_name')
        return Merchandise.objects.filter(category__name=category_name)


class MerchandiseDetailView(generics.RetrieveAPIView):
    queryset = Merchandise.objects.all()
    serializer_class = MerchandiseSerializer
