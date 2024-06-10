from rest_framework import serializers

from InventoryApp.models import Products, Size, Color


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Color
        fields="__all__"

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Size
        fields="__all__"

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Products
        fields="__all__"
