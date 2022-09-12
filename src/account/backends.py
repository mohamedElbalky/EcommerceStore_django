from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
# from .models import UserBase

UserModel = get_user_model()



class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # print(UserModel.objects.all())
            lookups = Q(username__iexact=username) | Q(email__iexact=username)
            user = UserModel.objects.get(lookups)
            print(user)
            if user.check_password(password):
                return user
            return None
        except UserModel.DoesNotExist:
            return None
        except:
            return None
            
    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

