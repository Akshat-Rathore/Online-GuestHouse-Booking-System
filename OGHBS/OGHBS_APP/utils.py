from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class AppTokenGenerator(PasswordResetTokenGenerator):   #generates token based on parameters of user id and time of registration
    def _make_hash_value(self,user,timestamp):
        return (text_type(user.is_active) + text_type(user.pk)+text_type(timestamp))

token_generator=AppTokenGenerator()