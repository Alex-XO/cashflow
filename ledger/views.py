from django_filters import rest_framework as df
from rest_framework import viewsets, filters
from .models import CashflowRecord
from .serializers import CashflowRecordSerializer
from catalog.models import Status, Type, Category, Subcategory

class CashflowRecordFilter(df.FilterSet):
    # ?record_date_after=YYYY-MM-DD&record_date_before=YYYY-MM-DD
    record_date = df.DateFromToRangeFilter(field_name="record_date")
    status = df.ModelChoiceFilter(queryset=Status.objects.all())
    type = df.ModelChoiceFilter(queryset=Type.objects.all())
    category = df.ModelChoiceFilter(queryset=Category.objects.all())
    subcategory = df.ModelChoiceFilter(queryset=Subcategory.objects.all())

    class Meta:
        model = CashflowRecord
        fields = ["record_date", "status", "type", "category", "subcategory"]

class CashflowRecordViewSet(viewsets.ModelViewSet):
    queryset = CashflowRecord.objects.select_related(
        "status", "type", "category", "subcategory"
    ).all()
    serializer_class = CashflowRecordSerializer
    filter_backends = [df.DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CashflowRecordFilter
    ordering_fields = ["record_date", "amount", "id"]
    search_fields = ["comment"]