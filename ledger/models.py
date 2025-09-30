from datetime import date, timedelta
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from catalog.models import Type, Status, Category, Subcategory


class CashflowRecord(models.Model):
    record_date = models.DateField("Дата", default=timezone.now)
    status = models.ForeignKey(Status, verbose_name="Статус", on_delete=models.PROTECT)
    type = models.ForeignKey(Type, verbose_name="Тип", on_delete=models.PROTECT)
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.PROTECT)
    subcategory = models.ForeignKey(Subcategory, verbose_name="Подкатегория", on_delete=models.PROTECT)
    amount = models.DecimalField("Сумма",
                                 max_digits=12,
                                 decimal_places=2,
                                 validators=[MinValueValidator(Decimal("0.01"))])
    comment = models.TextField("Комментарий", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-record_date", "-id"]
        constraints = [
            models.CheckConstraint(check=models.Q(amount__gt=Decimal("0")), name="amount_gt_0"),
        ]
        indexes = [
            models.Index(fields=["record_date"]),
            models.Index(fields=["status"]),
            models.Index(fields=["type"]),
            models.Index(fields=["category"]),
            models.Index(fields=["subcategory"]),
        ]

    def clean(self):
        if self.record_date:
            min_d = date(2000, 1, 1)
            max_d = date.today() + timedelta(days=365)
            if not (min_d <= self.record_date <= max_d):
                raise ValidationError({"record_date": "Дата вне допустимого диапазона."})
        if self.category_id and self.type_id and self.category.type_id != self.type_id:
            raise ValidationError({"category": "Категория не относится к выбранному типу."})
        if self.subcategory_id and self.category_id and self.subcategory.category_id != self.category_id:
            raise ValidationError({"subcategory": "Подкатегория не принадлежит выбранной категории."})

    def __str__(self):
        return f"{self.record_date} | {self.type} | {self.category}/{self.subcategory} | {self.amount}"
