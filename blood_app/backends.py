from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class EmailBackend(ModelBackend):
    """
    Authenticates users using their email address and password.
    Also falls back to username if needed.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        lookup = kwargs.get('email') or username
        if not lookup or not password:
            return None

        # Case-insensitive lookup by email
        user = UserModel.objects.filter(email__iexact=lookup).first()
        if not user:
            # Fallback to username
            user = UserModel.objects.filter(username__iexact=lookup).first()

        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
