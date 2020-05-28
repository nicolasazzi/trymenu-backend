
from django.db.models import Q

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from restaurant.models import Restaurant
from restaurant.serializers import RestaurantSerializer
from restaurant.views import pagination_maker, get_offset_limit

from account.models import Account
from account.serializers import AccountSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search(request):

    data = {}

    search_term = request.GET['q']
    tags = request.GET['type'].split(",")
    
    offset, limit = get_offset_limit(request=request)


    for tag in tags:

        addition = '&q=' + search_term + '&type=' + tag

        if tag == 'restaurant':

            restaurants = Restaurant.objects.filter(name__icontains = search_term)[offset:offset+limit+1]
          
            next = pagination_maker(request=request, offset=offset, limit=limit, more=restaurants[limit:])
            restaurant_list = []

            for restaurant in restaurants[:limit]:

                restaurant_serializer = RestaurantSerializer(restaurant)
                restaurant_list.append(restaurant_serializer.data)

            data['restaurants'] = {'items' : restaurant_list}
            data['restaurants']['next'] = next


        elif tag == 'user':
            
            accounts = Account.objects.filter(
                Q(first_name__icontains=search_term) | Q(last_name__icontains=search_term)
                )[offset:offset+limit+1]

            next = pagination_maker(request=request, offset=offset, limit=limit, more=accounts[limit:])

            accounts_list = []

            for account in accounts:

                account_serializer = AccountSerializer(account)
                accounts_list.append(account_serializer.data)

            data['users'] = {'items' : accounts_list}
            data['users']['next'] = next


    return Response(data)