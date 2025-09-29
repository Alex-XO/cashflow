from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
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
        qs = Category.objects.select_related("type").all().order_by("name")
        type_id = self.request.query_params.get("type")
        if type_id:
            qs = qs.filter(type_id=type_id)
        return qs

class SubcategoryViewSet(viewsets.ModelViewSet):
    serializer_class = SubcategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["category"]
    search_fields = ["name"]

    def get_queryset(self):
        qs = Subcategory.objects.select_related("category", "category__type").all().order_by("name")
        category_id = self.request.query_params.get("category")
        if category_id:
            qs = qs.filter(category_id=category_id)
        return qs