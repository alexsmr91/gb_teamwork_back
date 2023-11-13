from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter

from common.pagination import StandardResultsSetPagination
from .models import Message
from .serializers import MessageSerializer


class MessageAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    queryset = Message.objects.values(
        'text',
        'from_user',
        'to_user',
        'created_at',
        'updated_at',
    )
    serializer_class = MessageSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = [
        'created_at',
        'updated_at',
    ]

    def get_queryset(self):
        instance = super().get_queryset()
        return instance.filter(
            Q(from_user=self.request.user) | Q(to_user=self.request.user)
        )
