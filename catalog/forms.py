from django import forms
from .models import Type, Status, Category, Subcategory


class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ["name"]
        widgets = {"name": forms.TextInput(attrs={"class": "form-control"})}

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ["name"]
        widgets = {"name": forms.TextInput(attrs={"class": "form-control"})}

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "type"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "type": forms.Select(attrs={"class": "form-select"}),
        }

class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ["name", "category"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
        }
