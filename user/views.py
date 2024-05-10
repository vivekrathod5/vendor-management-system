import jwt
from drf_yasg import openapi
from django.conf import settings
from django.http import JsonResponse
from user.models import User, UserToken
from rest_framework.views import APIView
from user.helper import generate_access_token
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import check_password
from drf_yasg.utils import swagger_auto_schema
from user.serializers import LoginSerializer, UserSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Endpoint for user login",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='admin@example.com'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Admin@123'),
            },
            required=['email', 'password'],
        ),
        responses={200: UserSerializer()}
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
        
            if email is None or password is None:
                return JsonResponse({'error': 'Invalid credentials'}, status=400)
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=400)
            
            if check_password(password, user.password):
                data = {
                    'email': user.email,
                    'token': generate_access_token(user)
                }
                return JsonResponse({'message': 'Login successful', "data":data})
            else:
                return JsonResponse({'message': 'Invalid credentials.'}, status=400)
        return JsonResponse({'error': 'Invalid credentials..'}, status=400)




class LogoutView(APIView):
    @swagger_auto_schema(
        operation_description="Endpoint for user logout",
        responses={200: "Logout successful"},
        security=[{"Bearer": []}]
    )
    def get(self, request):
        header = request.headers.get('Authorization')
        access_token = header.split(' ')[1]
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
        token_id = payload['token_id']
        UserToken.objects.filter(id=token_id).update(is_active=False)
        return JsonResponse({'message': 'Logout successful'})
