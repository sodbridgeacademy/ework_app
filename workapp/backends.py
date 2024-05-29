from django.contrib.auth.backends import ModelBackend
#from django.contrib.auth import get_user_model
from .models import User

#User = get_user_model()

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Check if the user is logging in with a matric number
            if username.isdigit():
                user = User.objects.get(matric_number=username)
            else:
                user = User.objects.get(username=username)
            
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
