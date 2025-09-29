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

    def validate(self, attrs):
        instance = getattr(self, "instance", None)
        category = attrs.get("category", getattr(instance, "category", None))
        type_ = attrs.get("type", getattr(instance, "type", None))
        subcategory = attrs.get("subcategory", getattr(instance, "subcategory", None))

        if category is not None and type_ is not None:
            if category.type_id != type_.id:
                raise serializers.ValidationError({"category": "Категория не относится к выбранному типу."})
        if subcategory is not None and category is not None:
            if subcategory.category_id != category.id:
                raise serializers.ValidationError({"subcategory": "Подкатегория не принадлежит выбранной категории."})

        return attrs
