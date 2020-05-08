
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from .serializers import AccountRegistrationSerializer

@api_view(['POST',])
def registration_view(request):

    serializer = AccountRegistrationSerializer(data = request.POST)

    if serializer.is_valid():
        account = serializer.save()

        data = {}
        data['response'] = 'user successfully registered'

        data['email'] = account.email
        data['username'] = account.username
        data['first_name'] = account.first_name
        data['last_name'] = account.last_name
        
        token = Token.objects.get(user=account).key
        data['token'] = token

    else:
        print('not valid')
        data = serializer.errors

    return Response(data)

