import secrets
import urllib.parse
from datetime import datetime
import httpx

from rest_framework.authtoken.models import Token

from hhd.user_settings import BOT_TOKEN, CHAT_ID
from user_app import models


async def send_sms(phone, code):
    text = f"Номер телефона: {phone}\nКод: {code}"
    async with httpx.AsyncClient() as client:
        response = await client.get(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={urllib.parse.quote(text)}')


def get_code(phone):
    user_qs = models.User.objects.filter(username=phone)
    if len(user_qs) == 0:
        user = models.User.objects.create_user(
            username=f'{phone}',
            password=secrets.token_urlsafe(60),
        )
        user.save()
    elif len(user_qs) == 1:
        user = user_qs[0]
    else:
        return None
    user_profile = user.profile
    sending_time = user_profile.sending_time
    sending_time_delta = (datetime.now() - sending_time.replace(tzinfo=None)).seconds if sending_time is not None else 70
    if user is not None and user_profile.is_guest and user.username.isdigit and (user_profile.phone_code is None or 60 < sending_time_delta):
        user_profile.sending_time = datetime.now()
        user_profile.phone_code = secrets.SystemRandom().randrange(1000, 9999)
        user_profile.auth_attempts = 0
        user_profile.save()
        return user_profile.phone_code
    return None


def code_auth_validator(body):
    if 'phone' in body and 'code' in body:
        users = models.User.objects.filter(username=body['phone'])
        user = users[0] if len(users) == 1 else None
        user_profile = user.profile if user is not None else None
        if user is not None and user.profile.phone_code == body['code']:
            sending_time = user_profile.sending_time
            sending_time_delta = (datetime.now() - sending_time.replace(
                tzinfo=None)).seconds if sending_time is not None else 121
            auth_attempts = user_profile.auth_attempts
            if sending_time_delta < 300 and auth_attempts < 5:
                user_profile.auth_attempts = 0
                user_profile.phone_code = None
                user_profile.save()
                return ({
                    'token': Token.objects.get_or_create(
                        user=user,
                        defaults={
                            'key': Token.generate_key()
                        }
                    )[0].key
                }, 200)
            user_profile.save()
            return ({
                'error': 'try later',
                'attempts_left': 5 - user_profile.auth_attempts if user_profile.auth_attempts < 5 else 0
            }, 400)
        else:
            if user_profile is not None:
                user_profile.auth_attempts = user_profile.auth_attempts + 1
                user_profile.save()
                return ({
                    'status': 'bad request',
                    'attempts_left': 5 - user_profile.auth_attempts if user_profile.auth_attempts < 5 else 0
                }, 400)
    return ({
        'status': 'bad request'
    }, 400)
