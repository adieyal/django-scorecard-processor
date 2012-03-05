from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

class EmailModelBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        kwargs = {'email__iexact': username}
        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
                return None
