from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import CashflowRecord
from .forms import CashflowRecordForm
from catalog.models import Status, Type  # нужно для выпадающих списков


class RecordListView(ListView):
    model = CashflowRecord
    template_name = "records/list.html"
    context_object_name = "records"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().select_related("status", "type", "category", "subcategory")
        p = self.request.GET
        a = p.get("record_date_after")
        b = p.get("record_date_before")
        if a:
            qs = qs.filter(record_date__gte=a)
        if b:
            qs = qs.filter(record_date__lte=b)
        for f in ["status", "type", "category", "subcategory"]:
            v = p.get(f)
            if v:
                qs = qs.filter(**{f"{f}_id": v})
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["statuses"] = Status.objects.order_by("name")
        ctx["types"] = Type.objects.order_by("name")
        sel = {}
        for f in ["status", "type", "category", "subcategory"]:
            v = self.request.GET.get(f)
            try:
                sel[f] = int(v) if v else None
            except (TypeError, ValueError):
                sel[f] = None
        ctx["selected"] = sel
        return ctx


class RecordCreateView(CreateView):
    model = CashflowRecord
    form_class = CashflowRecordForm
    template_name = "records/form.html"
    success_url = reverse_lazy("record_list")


class RecordUpdateView(UpdateView):
    model = CashflowRecord
    form_class = CashflowRecordForm
    template_name = "records/form.html"
    success_url = reverse_lazy("record_list")


class RecordDeleteView(DeleteView):
    model = CashflowRecord
    template_name = "_confirm_delete_generic.html"
    success_url = reverse_lazy("record_list")