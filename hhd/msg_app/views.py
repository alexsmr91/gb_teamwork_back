from django.db.models import Q
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from rest_framework.authentication import SessionAuthentication

from common.pagination import StandardResultsSetPagination
from .models import Message
from .serializers import MessageSerializer


class MessageViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    authentication_classes = [SessionAuthentication]
    serializer_class = MessageSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = [
        'created_at',
        'updated_at',
    ]

    def get_queryset(self):
        # instance = super().get_queryset()
        return Message.objects.filter(
            Q(from_user=self.request.user) | Q(to_user=self.request.user)
        )
