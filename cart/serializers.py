from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Item

class ItemSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ("id", "SKU", "name", "in_stock", "total_amount", "category")

class CartItemSerializer(serializers.ModelSerializer):
    item = ItemSlimSerializer(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.all(), source="item", write_only=True
    )

    class Meta:
        model = CartItem
        fields = ("id", "item", "item_id", "quantity", "added_at")

class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ("id", "user", "cart_items")
        read_only_fields = ("user",)
