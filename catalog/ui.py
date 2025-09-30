from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Type, Status, Category, Subcategory
from .forms import TypeForm, StatusForm, CategoryForm, SubcategoryForm


class CrudMixin:
    list_url_name = None
    title_new = "Новая запись"
    title_edit = "Редактирование"

    def get_cancel_url(self):
        return reverse_lazy(self.list_url_name) if self.list_url_name else "/"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        is_edit = getattr(self, "object", None) and getattr(self.object, "pk", None)
        ctx["title"] = self.title_edit if is_edit else self.title_new
        ctx["cancel_url"] = self.get_cancel_url()
        return ctx

class SafeDeleteMixin(CrudMixin):
    entity_name = "объект"

    # Перехватываем удаление, чтобы поймать ProtectedError
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, f"{self.entity_name.capitalize()} удалён.")
        except ProtectedError:
            messages.error(request, f"Невозможно удалить: {self.entity_name} используется в существующих записях.")
        return redirect(self.get_cancel_url())

class CatalogHomeView(TemplateView):
    template_name = "catalog/index.html"

class TypeListView(ListView):
    model = Type
    template_name = "catalog/types_list.html"
    context_object_name = "items"
    paginate_by = 20

class TypeCreateView(CrudMixin, CreateView):
    model = Type
    form_class = TypeForm
    template_name = "_form_generic.html"
    success_url = reverse_lazy("types_list")
    list_url_name = "types_list"
    title_new = "Новый тип"

class TypeUpdateView(CrudMixin, UpdateView):
    model = Type
    form_class = TypeForm
    template_name = "_form_generic.html"
    success_url = reverse_lazy("types_list")
    list_url_name = "types_list"
    title_edit = "Изменить тип"

class TypeDeleteView(SafeDeleteMixin, DeleteView):
    model = Type
    template_name = "_confirm_delete_generic.html"
    success_url = reverse_lazy("types_list")
    list_url_name = "types_list"
    entity_name = "Тип"

class StatusListView(ListView):
    model = Status
    template_name = "catalog/statuses_list.html"
    context_object_name = "items"
    paginate_by = 20

class StatusCreateView(CrudMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = "_form_generic.html"
    success_url = reverse_lazy("statuses_list")
    list_url_name = "statuses_list"
    title_new = "Новый статус"

class StatusUpdateView(CrudMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = "_form_generic.html"
    success_url = reverse_lazy("statuses_list")
    list_url_name = "statuses_list"
    title_edit = "Изменить статус"

class StatusDeleteView(SafeDeleteMixin, DeleteView):
    model = Status
    template_name = "_confirm_delete_generic.html"
    success_url = reverse_lazy("statuses_list")
    list_url_name = "statuses_list"
    entity_name = "Статус"

class CategoryListView(ListView):
    model = Category
    template_name = "catalog/categories_list.html"
    context_object_name = "items"
    paginate_by = 20


class CategoryCreateView(CrudMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "_form_generic.html"
    success_url = reverse_lazy("categories_list")
    list_url_name = "categories_list"
    title_new = "Новая категория"

class CategoryUpdateView(CrudMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "_form_generic.html"
    success_url = reverse_lazy("categories_list")
    list_url_name = "categories_list"
    title_edit = "Изменить категорию"

class CategoryDeleteView(SafeDeleteMixin, DeleteView):
    model = Category
    template_name = "_confirm_delete_generic.html"
    success_url = reverse_lazy("categories_list")
    list_url_name = "categories_list"
    entity_name = "Категория"

class SubcategoryListView(ListView):
    model = Subcategory
    template_name = "catalog/subcategories_list.html"
    context_object_name = "items"
    paginate_by = 20

class SubcategoryCreateView(CrudMixin, CreateView):
    model = Subcategory
    form_class = SubcategoryForm
    template_name = "_form_generic.html"
    success_url = reverse_lazy("subcategories_list")
    list_url_name = "subcategories_list"
    title_new = "Новая подкатегория"

class SubcategoryUpdateView(CrudMixin, UpdateView):
    model = Subcategory
    form_class = SubcategoryForm
    template_name = "_form_generic.html"
    success_url = reverse_lazy("subcategories_list")
    list_url_name = "subcategories_list"
    title_edit = "Изменить подкатегорию"

class SubcategoryDeleteView(SafeDeleteMixin, DeleteView):
    model = Subcategory
    template_name = "_confirm_delete_generic.html"
    success_url = reverse_lazy("subcategories_list")
    list_url_name = "subcategories_list"
    entity_name = "подкатегория"