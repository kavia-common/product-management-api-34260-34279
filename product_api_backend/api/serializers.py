from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product model to convert between model instances and JSON.
    """

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'quantity']
        read_only_fields = ['id']
