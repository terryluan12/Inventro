from rest_framework import serializers
from .models import Item, ItemCategory

class ItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCategory
        fields = ("id", "name")

class ItemSerializer(serializers.ModelSerializer):
    category = ItemCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ItemCategory.objects.all(), source="category", write_only=True
    )

    class Meta:
        model = Item
        fields = ("id", "SKU", "name", "in_stock", "total_amount", "category", "category_id")
