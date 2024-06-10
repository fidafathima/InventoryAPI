from django.contrib.auth import authenticate, login
from django.shortcuts import render
from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from InventoryApp import serializer
from InventoryApp.models import Products, Color, Size
from InventoryApp.serializer import ProductSerializer, ColorSerializer, SizeSerializer


# Create your views here.

class size(generics.ListCreateAPIView):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer


class color(generics.ListCreateAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer

class Product(generics.ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [IsAuthenticated]

    def product_create(self,serializer):
        serializer.save(CreatedUser=self.request.user)


class LoginView(views.APIView):
    def post(self, request, format= None):
        data = request.data

        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                print(user)
                return Response({'user': {'id': user.id, 'username': user.username,'password':user.password}}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Invalid credentials'},status=status.HTTP_404_NOT_FOUND)


class Product1(APIView):
    def get(self,request):
        data=Products.objects.all()
        serializer=ProductSerializer(data,many=True)
        return Response(serializer.data)

