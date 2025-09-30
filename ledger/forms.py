from datetime import date, timedelta
from django import forms
from django.core.exceptions import ValidationError

from .models import CashflowRecord
from catalog.models import Category, Subcategory


class CashflowRecordForm(forms.ModelForm):
    class Meta:
        model = CashflowRecord
        fields = ["record_date", "status", "type", "category", "subcategory", "amount", "comment"]
        widgets = {
            "record_date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control",
                "min": "1950-01-01",
                "max": (date.today() + timedelta(days=365)).isoformat(),
            }),
            "amount": forms.NumberInput(attrs={"step": "0.01", "min": "0.01", "class": "form-control"}),
            "comment": forms.Textarea(attrs={"rows": 2, "class": "form-control", "maxlength": 1000}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for n in ["status", "type", "category", "subcategory"]:
            self.fields[n].widget.attrs.update({"class": "form-select"})

        self.fields["category"].queryset = Category.objects.none()
        self.fields["subcategory"].queryset = Subcategory.objects.none()

        data = self.data or None
        inst = getattr(self, "instance", None)

        if data and data.get("type"):
            try:
                t_id = int(data.get("type"))
                self.fields["category"].queryset = Category.objects.filter(type_id=t_id).order_by("name")
            except (TypeError, ValueError):
                pass
        elif inst and inst.pk and inst.type_id:
            self.fields["category"].queryset = Category.objects.filter(type_id=inst.type_id).order_by("name")

        if data and data.get("category"):
            try:
                c_id = int(data.get("category"))
                self.fields["subcategory"].queryset = Subcategory.objects.filter(category_id=c_id).order_by("name")
            except (TypeError, ValueError):
                pass
        elif inst and inst.pk and inst.category_id:
            self.fields["subcategory"].queryset = Subcategory.objects.filter(category_id=inst.category_id).order_by("name")

    def clean(self):
        cleaned = super().clean()
        t = cleaned.get("type")
        c = cleaned.get("category")
        s = cleaned.get("subcategory")
        if t and c and c.type_id != t.id:
            self.add_error("category", "Категория не относится к выбранному типу.")
        if c and s and s.category_id != c.id:
            self.add_error("subcategory", "Подкатегория не принадлежит выбранной категории.")
        return cleaned

    def clean_comment(self):
        txt = (self.cleaned_data.get("comment") or "").strip()
        if len(txt) > 1000:
            raise ValidationError(f"Комментарий не длиннее 1000 символов.")
        return txt
