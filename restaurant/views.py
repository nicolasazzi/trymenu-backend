from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from .serializers import ItemSerializer, RestaurantSerializer, CategorySerializer
from .models import Restaurant


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def restaurants_request_view(request):


    if request.GET:
        
        try:
            limit = int(request.GET['limit'])
        except:
            limit = 20
        
        try:
            offset = int(request.GET['offset'])
        except:
            offset = 0


        restaurants = Restaurant.objects.all()[offset:limit]
        restaurant_data = []
        restaurant_counter = 0

        for restaurant in restaurants:

            categories = restaurant.categories.all()
            categories_data = []
            category_counter = 0

            for category in categories:

                items = category.items.filter(restaurant=restaurant)
                item_counter = 0
                item_data = []

                for item in items:

                    item_serializer = ItemSerializer(item)

                    try:
                        did_try = item.item_user_relation_set.get(account=request.user).did_try
                    except:
                        did_try = False

                    item_data.append(item_serializer.data)
                    item_data[item_counter]['did_try'] = did_try
                    item_counter += 1

                category_serializer = CategorySerializer(category)

                categories_data.append(category_serializer.data)
                categories_data[category_counter]['category_items'] = item_data

                category_counter += 1
                

            restaurant_serializer = RestaurantSerializer(restaurant)
            
            restaurant_data.append(restaurant_serializer.data)
            restaurant_data[restaurant_counter]['menu'] = categories_data
            restaurant_counter += 1

        offset +=  limit
        print(limit)
        data = {
            'restaurants' : restaurant_data,
            'next' : 'https://trymenu.herokuapp.com/api/restaurant/get_restaurants?limit=' + str(limit) + '&offset=' + str(offset)
        }

        return Response(data)

    else:
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
 