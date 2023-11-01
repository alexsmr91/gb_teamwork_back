from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

UserModel = get_user_model()


class CustomBackend(BaseBackend):
    @staticmethod
    def authenticate_by_sms(phone=None, code=None, **kwargs):
        try:
            user = UserModel.objects.get(phone=phone)
            if code:
                if user.otp == code:
                    print('Где то тут должна быть проверка таймаута кода')
                    return user
                else:
                    print('Где то тут должна быть проверка таймаута кода')
                    user.generate_code()
            else:
                user.generate_code()
        except UserModel.DoesNotExist:
            UserModel.objects.create(phone=phone)
        return None
