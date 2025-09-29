from rest_framework import serializers
from .models import Type, Status, Category, Subcategory


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ["id", "name"]

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ["id", "name"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "type"]

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ["id", "name", "category"]
