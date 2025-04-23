from django.views import View
from django.http import JsonResponse
from vault.dao import PasswordEntryDAO
import jwt
from django.conf import settings
from accounts.dao import UserDAO


class EntryListView(View):

    def get(self, request):
        """
        Handle GET requests to retrieve all password entries for the authenticated user.
        """
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({'error': 'Authorization token is missing'}, status=401)
        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']

            user = UserDAO.get_by_id(user_id)
            if not user:
                return JsonResponse({'error': 'Invalid or expired token'}, status=404)
            entries = PasswordEntryDAO.get_list(user_id)
            entry_list = [
                {
                    'id': entry.id,
                    'title': entry.title,
                    "encrypted_data": entry.encrypted_data,
                    'created_at': entry.created_at,
                    'updated_at': entry.updated_at,
                }
                for entry in entries
            ]
            return JsonResponse({'entries': entry_list}, status=200)
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token has expired'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid token'}, status=401)
        except Exception as e:  # Catch all other exceptions
            return JsonResponse({'error': str(e)}, status=500)
