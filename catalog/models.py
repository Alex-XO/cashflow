from django.db import models


class Type(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=64)
    type = models.ForeignKey(
        Type,
        on_delete=models.PROTECT,
        related_name="categories",
    )

    class Meta:
        unique_together = ("name", "type")

    def __str__(self):
        return f"{self.name} ({self.type})"

class Subcategory(models.Model):
    name = models.CharField(max_length=64)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="subcategories",
    )

    class Meta:
        unique_together = ("name", "category")

    def __str__(self):
        return f"{self.name} ({self.category})"
