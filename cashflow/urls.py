from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from catalog import views as catalog_api
from catalog import ui as catalog_ui
from ledger import views as ledger_api
from ledger import ui as ledger_ui

def check(_):
    return HttpResponse("OK")

router = DefaultRouter()
router.register(r"types", catalog_api.TypeViewSet)
router.register(r"statuses", catalog_api.StatusViewSet)
router.register(r"categories", catalog_api.CategoryViewSet, basename="category")
router.register(r"subcategories", catalog_api.SubcategoryViewSet, basename="subcategory")
router.register(r"records", ledger_api.CashflowRecordViewSet, basename="record")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("health/", check, name="health"),
    path("", ledger_ui.RecordListView.as_view(), name="record_list"),
    path("records/new/", ledger_ui.RecordCreateView.as_view(), name="record_create"),
    path("records/<int:pk>/edit/", ledger_ui.RecordUpdateView.as_view(), name="record_edit"),
    path("records/<int:pk>/delete/", ledger_ui.RecordDeleteView.as_view(), name="record_delete"),
    path("catalog/", catalog_ui.CatalogHomeView.as_view(), name="catalog_home"),

    path("catalog/types/", catalog_ui.TypeListView.as_view(), name="types_list"),
    path("catalog/types/new/", catalog_ui.TypeCreateView.as_view(), name="type_create"),
    path("catalog/types/<int:pk>/edit/", catalog_ui.TypeUpdateView.as_view(), name="type_edit"),
    path("catalog/types/<int:pk>/delete/", catalog_ui.TypeDeleteView.as_view(), name="type_delete"),

    path("catalog/statuses/", catalog_ui.StatusListView.as_view(), name="statuses_list"),
    path("catalog/statuses/new/", catalog_ui.StatusCreateView.as_view(), name="status_create"),
    path("catalog/statuses/<int:pk>/edit/", catalog_ui.StatusUpdateView.as_view(), name="status_edit"),
    path("catalog/statuses/<int:pk>/delete/", catalog_ui.StatusDeleteView.as_view(), name="status_delete"),

    path("catalog/categories/", catalog_ui.CategoryListView.as_view(), name="categories_list"),
    path("catalog/categories/new/", catalog_ui.CategoryCreateView.as_view(), name="category_create"),
    path("catalog/categories/<int:pk>/edit/", catalog_ui.CategoryUpdateView.as_view(), name="category_edit"),
    path("catalog/categories/<int:pk>/delete/", catalog_ui.CategoryDeleteView.as_view(), name="category_delete"),

    path("catalog/subcategories/", catalog_ui.SubcategoryListView.as_view(), name="subcategories_list"),
    path("catalog/subcategories/new/", catalog_ui.SubcategoryCreateView.as_view(), name="subcategory_create"),
    path("catalog/subcategories/<int:pk>/edit/", catalog_ui.SubcategoryUpdateView.as_view(), name="subcategory_edit"),
    path("catalog/subcategories/<int:pk>/delete/", catalog_ui.SubcategoryDeleteView.as_view(), name="subcategory_delete"),

]