import json
import jwt
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.conf import settings
from accounts.dao import UserDAO

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):
    """
    View to handle user registration.
    """
    def post(self, request):
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return JsonResponse({'error': 'Email and password are required.'}, status=400)

        if UserDAO.get_by_email(email):
            return JsonResponse({'error': 'Email already exists.'}, status=400)
        
        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return JsonResponse({'error': 'Invalid email format.'}, status=400)

        # Hash the password
        password_hash = make_password(password)

        # Create the user
        user = UserDAO.create_user(email=email, password_hash=password_hash)

        return JsonResponse({'message': 'User created successfully.', 'user_id': str(user.id)}, status=201)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    """
    View to handle user login.
    """
    def post(self, request):
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return JsonResponse({'error': 'Email and password are required.'}, status=400)

        # Authenticate the user
        user = authenticate(request, email=email, password=password)

        if user is None:
            return JsonResponse({'error': 'Invalid email or password.'}, status=401)

        # Generate JWT token
        token = jwt.encode({
            'user_id': str(user.id),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }, settings.SECRET_KEY, algorithm='HS256')

        return JsonResponse({'token': token}, status=200)
    
class UserView(View):
    """
    View to handle user-related operations.
    """
    def get(self, request):
        # Get the user ID from the JWT token
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return JsonResponse({'error': 'Token is required.'}, status=401)

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token has expired.'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid token.'}, status=401)

        # Retrieve the user
        user = UserDAO.get_by_id(user_id)
        
        if not user:
            return JsonResponse({'error': 'User not found.'}, status=404)

        entry_count = user.password_entries.count()

        # Return user details
        return JsonResponse({
            'email': user.email,
            'entry_count': entry_count
        }, status=200)