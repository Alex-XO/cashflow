from rest_framework import serializers
from .models import CashflowRecord


class CashflowRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashflowRecord
        fields = [
            "id",
            "record_date",
            "status",
            "type",
            "category",
            "subcategory",
            "amount",
            "comment",
            "created_at",
            "updated_at",
        ]

    def validate(self, data):
        inst = getattr(self, "instance", None)
        category = data.get("category", getattr(inst, "category", None))
        type_ = data.get("type", getattr(inst, "type", None))
        sub = data.get("subcategory", getattr(inst, "subcategory", None))

        if category and type_ and category.type_id != type_.id:
            raise serializers.ValidationError({"category": "Категория не относится к выбранному типу."})
        if sub and category and sub.category_id != category.id:
            raise serializers.ValidationError({"subcategory": "Подкатегория не принадлежит выбранной категории."})

        return data
