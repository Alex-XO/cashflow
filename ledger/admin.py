from django.contrib import admin
from .models import CashflowRecord


@admin.register(CashflowRecord)
class CashflowRecordAdmin(admin.ModelAdmin):
    list_display = ("record_date", "status", "type", "category", "subcategory", "amount", "short_comment", "created_at")
    list_filter = ("record_date", "status", "type", "category", "subcategory")
    search_fields = ("comment",)
    date_hierarchy = "record_date"
    ordering = ("-record_date", "-id")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": (("record_date", "amount"), ("status", "type"), ("category", "subcategory"), "comment")}),
        ("Служебные", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def short_comment(self, obj):
        text = obj.comment or ""
        return (text[:40] + "…") if len(text) > 40 else text

    short_comment.short_description = "Комментарий"
