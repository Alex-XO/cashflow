from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from catalog.models import Type, Status, Category, Subcategory


class CashflowRecord(models.Model):
    record_date = models.DateField(default=timezone.now)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    type = models.ForeignKey(Type, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    comment = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-record_date", "-id"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(amount__gt=Decimal("0")),
                name="amount_gt_0",
            ),
        ]
        indexes = [
            models.Index(fields=["record_date"]),
            models.Index(fields=["status"]),
            models.Index(fields=["type"]),
            models.Index(fields=["category"]),
            models.Index(fields=["subcategory"]),
        ]

    def clean(self):
        # Соответствие категория → тип
        if self.category_id and self.type_id:
            if self.category.type_id != self.type_id:
                raise ValidationError({"category": "Категория не относится к выбранному типу."})
        # Соответствие подкатегория → категория
        if self.subcategory_id and self.category_id:
            if self.subcategory.category_id != self.category_id:
                raise ValidationError({"subcategory": "Подкатегория не принадлежит выбранной категории."})

    def __str__(self):
        return f"{self.record_date} | {self.type} | {self.category}/{self.subcategory} | {self.amount}"