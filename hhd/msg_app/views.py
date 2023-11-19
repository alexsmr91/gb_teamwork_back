from django.db.models import Q, OuterRef, Subquery
from rest_framework import status
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.filters import SearchFilter

from common.pagination import StandardResultsSetPagination
from .models import Message
from .serializers import MessageSerializer, MessageCreateSerializer, MessagesFilterSerializer, ChatSerializer, User


class MessageViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        payload = MessagesFilterSerializer(data=self.request.GET)
        payload.is_valid(raise_exception=True)
        payload = payload.data
        if 'user_id' in payload and not self.request.user.profile.is_guest:
            queryset = Message.objects.filter(
                Q(from_user_id=payload['user_id']) | Q(to_user_id=payload['user_id'])
            )
        else:
            queryset = Message.objects.filter(
                Q(from_user=self.request.user) | Q(to_user=self.request.user)
            ).order_by('created_at')
        if 'last_message_id' in payload:
            last_message = Message.objects.get(pk=payload['last_message_id'])

            if 'history' in payload and payload['history']:
                queryset = queryset.filter(
                    created_at__lte=last_message.created_at
                ).exclude(pk=payload['last_message_id'])
            else:
                queryset = queryset.filter(
                    created_at__gte=last_message.created_at
                ).exclude(pk=payload['last_message_id'])
        last_ten_messages = queryset.order_by('-created_at')[:20]
        return reversed(last_ten_messages)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = Message.objects.get(pk=kwargs['pk'])
        except Message.DoesNotExist:
            raise NotFound
        serializer = self.get_serializer(instance)
        if request.user.profile.is_guest:
            if instance.from_user == request.user or instance.to_user == request.user:
                return Response(serializer.data)
            else:
                raise NotFound
        else:
            return Response(serializer.data)


class MessageCreateViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        Message.objects.create(
            from_user_id=request.user.id,
            to_user_id=serializer.data['to_user'] if 'to_user' in serializer.data and not request.user.profile.is_guest else None,
            text=serializer.data['text']
        )
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ChatListViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer
    filter_backends = [SearchFilter]
    search_fields = [
        'username',
        'first_name',
    ]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        if self.request.user.profile.is_guest:
            raise PermissionDenied
        else:
            messages = Message.objects.filter(
                Q(from_user_id=OuterRef('pk')) | Q(to_user_id=OuterRef('pk'))
            ).order_by('-created_at')
            return User.objects.annotate(
                last_message=Subquery(messages.values_list('text', flat=False)),
                last_message_date=Subquery(messages.values_list('created_at', flat=False)[:1]),
                from_user_id=Subquery(messages.values_list('from_user_id', flat=False)[:1]),
                is_guest_sender=Subquery(messages.values_list('from_user__profile__is_guest', flat=False)[:1]),
            ).filter(profile__is_guest=True, last_message__isnull=False).values(
                'id',
                'username',
                'first_name',
                'last_message',
                'last_message_date',
                'is_guest_sender',
                'from_user_id'
            ).order_by('-last_message_date')
