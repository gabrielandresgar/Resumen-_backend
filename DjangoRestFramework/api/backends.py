from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, correo=None, password=None, **kwargs):
        UserModel = get_user_model()
        
        try:
            user = UserModel.objects.get(correo=correo)
        except UserModel.DoesNotExist:
            return None
        
        
        if user.password == password:
           return user
        return None
