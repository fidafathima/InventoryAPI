from django.contrib.auth import authenticate, login
from django.http import Http404
from django.shortcuts import render
from rest_framework import generics, status, views
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from InventoryApp import serializer
from InventoryApp.models import ProductDetails, Customer, Cart, Delivery, PaymentMethod, Order
from InventoryApp.serializer import ProductSerializer, LoginSerializer, CartSerializer, OrderSerializer, \
    DeliverySerializer, PaymentSerializer


# Create your views here.


class Product(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer=ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):

    def post(self, request):
        data = request.data

        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                # login(request, user)
                token, created = Token.objects.get_or_create(user=user)

                if user.is_staff:

                    return Response({'user': {'id': user.id, 'username': user.username},'access':{'token': token.key}},status=status.HTTP_200_OK)

                elif user.is_customer:

                    return Response({'user': {'id': user.id, 'username': user.username},'access':{'token': token.key}},status=status.HTTP_200_OK)

                else:
                    return Response({'error': 'Invalid credentials'},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Invalid credentials'},status=status.HTTP_404_NOT_FOUND)


class Product1(APIView):
    def get(self,request):
        data=ProductDetails.objects.all()
        serializer=ProductSerializer(data,many=True)
        return Response(serializer.data)

class PDetail(APIView):
    def get_object(self,id):
        try:
            return ProductDetails.objects.get(id=id)
        except ProductDetails.DoesNotExist:
            raise Http404

    def get(self, request, id):
        customer = self.get_object(id)
        serializer = ProductSerializer(customer)
        return Response(serializer.data)


class customer(APIView):
    def get(self,request):
        data=Customer.objects.all()
        serializer=LoginSerializer(data,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            customer=serializer.save()
            customer.is_customer = True
            customer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddToCart(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self,id):
        try:
            return ProductDetails.objects.get(id=id)
        except ProductDetails.DoesNotExist:
            raise Http404

    def post(self, request, id):
        product = self.get_object(id)
        user = request.user
        print(user)

        if not user:
            return Response({'detail': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        # Check if the item already exists in the cart
        try:
            cart_item = Cart.objects.get(user=user, item=product)
            if int(cart_item.quantity0) >= cart_item.item.TotalStock:
                return Response({'detail': 'Item out of stock'}, status=status.HTTP_400_BAD_REQUEST)

            else:
                cart_item.quantity0 = int(cart_item.quantity0) + 1
                if cart_item.status=="1":
                    cart_item.status=0
                cart_item.save()
                return Response({'detail': 'Cart updated'}, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            # Create a new cart item
            Cart.objects.create(user=user, item=product)
            return Response({'detail': 'Item added to cart'}, status=status.HTTP_201_CREATED)


class CartView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user=request.user
        data=Cart.objects.filter(user=user)
        serializer=CartSerializer(data,many=True)
        return Response(serializer.data)


class ChangeQuantity(APIView):
    # permission_classes = [IsAuthenticated]

    def get_object(self, id):
        try:
            return Cart.objects.get(id=id)
        except Cart.DoesNotExist:
            raise Http404

    def post(self,request,id):
        item=self.get_object(id)
        if int(item.quantity0)<=item.item.TotalStock :
            item.quantity0=int(item.quantity0)+1
            item.save()
            serializer=CartSerializer(item)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response('item out of stock', status=status.HTTP_400_BAD_REQUEST)


class Remove(APIView):
    # permission_classes = [IsAuthenticated]

    def get_object(self, id):
        try:
            return Cart.objects.get(id=id)
        except Cart.DoesNotExist:
            raise Http404

    def post(self,request,id):
        item=self.get_object(id)
        item.quantity0=int(item.quantity0)-1
        item.save()
        serializer=CartSerializer(item)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

class RemoveItem(APIView):
    # permission_classes = [IsAuthenticated]

    def get_object(self, id):
        try:
            return Cart.objects.get(id=id)
        except Cart.DoesNotExist:
            raise Http404

    def post(self,request,id):
        item=self.get_object(id)
        item.status=1
        item.save()
        serializer=CartSerializer(item)
        return Response(serializer.data,status=status.HTTP_201_CREATED)


class address(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = DeliverySerializer(data=request.data)
        serializer2= PaymentSerializer(data=request.data)
        if serializer.is_valid() and  serializer2.is_valid():
            serializer.save()
            serializer2.save()
            return Response({
                "delivery": serializer.data,
                "payment": serializer2.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "delivery_errors": serializer.errors,
            "payment_errors": serializer2.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        user = request.user
        address1 = Delivery.objects.filter(user=user)
        serializer=DeliverySerializer(address1,many=True)
        return Response({
                "delivery": serializer.data,
            })



class CheckOut(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        user=request.user
        data=Cart.objects.filter(user=user)
        address1 = Delivery.objects.get(user=user)
        payment1 = PaymentMethod.objects.get(user=user)
        cart = [i for i in data]
        order = Order.objects.create(user=user, delivery=address1, payment=payment1)
        if cart:
            for i in cart:
                if i.status == "0":
                    order.product.add(i)
                    i.item.quantity = i.item.quantity - int(i.quantity0)
                    i.item.save()
                    i.status = 1
                    i.save()
        serializer=OrderSerializer(order,many=True)
        return Response(serializer.data)


class ChangeAddress(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        customer = Delivery.objects.get(id=id)
        print(customer)
        serializer = DeliverySerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class upi(APIView):
#     # permission_classes = [IsAuthenticated]
#
#     def get_object(self, id):
#         try:
#             return PaymentMethod.objects.get(id=id)
#         except PaymentMethod.DoesNotExist:
#             raise Http404
#
#     def post(self,request,id):
#         item=self.get_object(id)
#         item.UPI_Payment=True
#         item.save()
#         serializer=PaymentSerializer(item)
#         return Response(serializer.data,status=status.HTTP_201_CREATED)
