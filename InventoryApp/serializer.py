from rest_framework import serializers

from InventoryApp.models import ProductDetails, Customer, Cart, Order, PaymentMethod, Delivery


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model=ProductDetails
        fields="__all__"



class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model=Customer
        fields=('username', 'email', 'password', 'password2')

    def create(self, validated_data):
        user = Customer.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class CartSerializer(serializers.ModelSerializer):
    item = ProductSerializer()
    user = LoginSerializer()
    class Meta:
        model=Cart
        fields="__all__"


class DeliverySerializer(serializers.ModelSerializer):
    # user = LoginSerializer()
    user = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    class Meta:
        model=Delivery
        fields="__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model=PaymentMethod
        fields="__all__"


class OrderSerializer(serializers.ModelSerializer):
    # delivery = DeliverySerializer()
    # user = LoginSerializer()
    # payment=PaymentSerializer()
    # product = CartSerializer(many=True)
    class Meta:
        model=Order
        fields="__all__"