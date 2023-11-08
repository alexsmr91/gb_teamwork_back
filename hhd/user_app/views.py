import asyncio
import json
from asgiref.sync import sync_to_async

from django.http import JsonResponse
from rest_framework.decorators import api_view

from common.utils import get_code, send_sms, code_auth_validator


class ProfileAPIView():
    pass


async def send_sms_view(request, phone=''):
    loop = asyncio.get_event_loop()
    async_get_code = sync_to_async(get_code)
    code = await async_get_code(phone)
    if code is None:
        return JsonResponse({'status': 'forbidden'}, status=403)
    else:
        loop.create_task(send_sms(phone, code))
        return JsonResponse({'status': 'created'}, status=201)


@api_view(['POST'])
def get_auth_token_with_code_view(request):
    body = json.loads(request.body.decode('utf-8'))
    response, status = code_auth_validator(body)
    return JsonResponse(response, status=status)
