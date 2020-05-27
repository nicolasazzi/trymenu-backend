
from django.db.models import Q

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from restaurant.models import Restaurant
from restaurant.serializers import RestaurantSerializer
from restaurant.views import pagination_maker

from account.models import Account
from account.serializers import AccountSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search(request):

    data = {}

    search_term = request.GET['q']
    tags = request.GET['type'].split(",")
    

    try:
        limit = int(request.GET['limit'])
    except:
        limit = 20
    
    try:
        offset = int(request.GET['offset'])
    except:
        offset = 0


    for tag in tags:

        addition = '&q=' + search_term + '&type=' + tag
        next = pagination_maker(request=request, offset=offset, limit=limit)

        if tag == 'restaurant':

            restaurants = Restaurant.objects.filter(name__icontains = search_term)[offset:offset+limit]
            restaurant_list = []

            for restaurant in restaurants:

                restaurant_serializer = RestaurantSerializer(restaurant)
                restaurant_list.append(restaurant_serializer.data)

            data['restaurants'] = {'items' : restaurant_list}
            data['restaurants']['next'] = next


        elif tag == 'user':

            accounts = Account.objects.filter(
                Q(first_name__icontains=search_term) | Q(last_name__icontains=search_term)
                )[offset:offset+limit]

            print(accounts)

            accounts_list = []

            for account in accounts:

                account_serializer = AccountSerializer(account)
                accounts_list.append(account_serializer.data)

            data['users'] = {'items' : accounts_list}
            data['users']['next'] = next


    return Response(data)