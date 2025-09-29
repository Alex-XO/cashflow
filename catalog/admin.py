from django.contrib import admin
from .models import Type, Status, Category, Subcategory


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "type")
    list_filter = ("type",)
    search_fields = ("name",)
    ordering = ("type__name", "name")


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    list_filter = ("category",)
    search_fields = ("name",)
    ordering = ("category__name", "name")