from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from .serializers import AccountRegistrationSerializer

@api_view(['POST',])
def registration_view(request):

    serializer = AccountRegistrationSerializer(data = request.data)

    if serializer.is_valid():
        account = serializer.save()

        data = {}
        data['response'] = 'user successfully registered'
        user = {
            'email' : account.email,
            'username' : account.username,
            'first_name' : account.first_name,
            'last_name' : account.last_name, 
        }
        
        data['user'] = user

        token = Token.objects.get(user=account).key
        data['token'] = token

        return Response(data)

    else:
        print('not valid')
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

