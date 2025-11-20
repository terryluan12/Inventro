from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem
from .serializers import CartSerializer
from inventory.models import Item


class CartViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user carts.
    - Requires authentication
    - Users can only access their own cart
    - Provides endpoints to add/remove/update items
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Only return the current user's cart"""
        return Cart.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Automatically assign cart to current user"""
        serializer.save(user=self.request.user)
    
    def get_object(self):
        """Get or create user's cart"""
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart
    
    @action(detail=True, methods=['post'])
    def remove_item(self, request, pk=None):
        """
        Remove item from cart.
        POST /api/cart/{id}/remove_item/
        Body: {"item_id": 1}
        """
        cart = self.get_object()
        item_id = request.data.get('item_id')
        
        if not item_id:
            return Response(
                {'error': 'item_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        deleted_count, _ = CartItem.objects.filter(
            cart=cart,
            item_id=item_id
        ).delete()
        
        if deleted_count == 0:
            return Response(
                {'error': 'Item not found in cart'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def clear(self, request, pk=None):
        """
        Clear all items from cart.
        POST /api/cart/{id}/clear/
        """
        cart = self.get_object()
        cart.cart_items.all().delete()
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)