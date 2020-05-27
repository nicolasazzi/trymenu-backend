from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token


from .serializers import ItemSerializer, RestaurantSerializer, CategorySerializer, TryItemSerializer
from .models import Restaurant, Item_User_Relation, Item


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def restaurants_request_view(request):

    try:
        limit = int(request.GET['limit'])
    except:
        limit = 20
    
    try:
        offset = int(request.GET['offset'])
    except:
        offset = 0
    
    restaurants = Restaurant.objects.all()[offset:offset+limit]

    data = get_restaurant_contents(request=request, restaurants=restaurants)

    next = pagination_maker(request=request, offset=offset, limit=limit)
    data['next'] = next
    return Response(data)


def get_restaurant_contents(request, restaurants):
    
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
                    item.item_user_relation_set.get(account=request.user)
                    did_try = True
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


    data = {
        'restaurants' : restaurant_data,
    }

    return Response(data)


def pagination_maker(request, offset, limit, default_next_additive = ''):

    offset +=  limit

    if Restaurant.objects.all()[offset:offset+limit]:
        next = request.path + '?offset=' + str(offset) + '&limit=' + str(limit) + default_next_additive
        return next
    else:
        return ''



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def try_item(request):
    
    try_item_serializer = TryItemSerializer(request.data)
    try:
        item_tried = Item.objects.get(id = try_item_serializer.data['id'])
    except:
        return Response(status.HTTP_400_BAD_REQUEST)
    
    item_user_relation = Item_User_Relation(
        account = request.user, item=item_tried
    )

    item_user_relation.save()

    return Response({'did_try' : True})