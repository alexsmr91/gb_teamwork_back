import asyncio
import json
from asgiref.sync import sync_to_async

from django.http import JsonResponse, Http404
from django.db.models import F
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.utils import get_code, send_sms, code_auth_validator
from .models import Profile
from .serializers import ProfileSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_api_view(request):
    try:
        instance = Profile.objects.annotate(
            username=F('user__username'),
            is_superuser=F('user__is_superuser')
        ).values(
            'username',
            'chat_room',
            'is_guest',
            'is_superuser',
        ).get(user=request.user)
    except Profile.DoesNotExist:
        return Http404
    else:
        serializer = ProfileSerializer(instance)
        return Response(serializer.data)


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
