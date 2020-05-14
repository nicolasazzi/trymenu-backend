from rest_framework import serializers

from .models import Restaurant, Item, Category


class RestaurantRequestSerializer(serializers.Serializer):

    limit = serializers.IntegerField(required=False)
    offset = serializers.IntegerField(required=False)



class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'price']


class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ['id', 'location']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']