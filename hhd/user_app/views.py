from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import mixins

from .serializers import ProfileSerializer
from .pagination import StandardResultsSetPagination
from .models import Profile


class UserListAPIViewSet(mixins.ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ProfileSerializer
    pagination_class = StandardResultsSetPagination
    queryset = Profile.objects.all()
