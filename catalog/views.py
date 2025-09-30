from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from .models import Type, Status, Category, Subcategory
from .serializers import TypeSerializer, StatusSerializer, CategorySerializer, SubcategorySerializer


class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all().order_by("name")
    serializer_class = TypeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all().order_by("name")
    serializer_class = StatusSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["type"]
    search_fields = ["name"]

    def get_queryset(self):
        qs = Category.objects.select_related("type").order_by("name")
        t = self.request.query_params.get("type")
        return qs.filter(type_id=t) if t else qs

class SubcategoryViewSet(viewsets.ModelViewSet):
    serializer_class = SubcategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["category"]
    search_fields = ["name"]

    def get_queryset(self):
        qs = Subcategory.objects.select_related("category", "category__type").order_by("name")
        c = self.request.query_params.get("category")
        return qs.filter(category_id=c) if c else qs