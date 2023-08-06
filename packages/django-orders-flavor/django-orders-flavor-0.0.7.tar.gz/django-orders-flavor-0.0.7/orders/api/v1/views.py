from rest_framework import permissions as api_permissions
from rest_framework import viewsets

from ... import models
from .. import permissions, serializers


class OrderViewSet(viewsets.ModelViewSet):
    lookup_value_regex = '[0-9a-f]{32}'

    permission_classes = (
        api_permissions.IsAuthenticated,
        permissions.IsStaffOrOwner)

    def get_queryset(self):
        qs = models.Order.objects.all()

        if not self.request.user.is_staff:
            return qs.filter(user=self.request.user)
        return qs

    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return serializers.OrderWriteOnlySerializer
        return serializers.OrderReadOnlySerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
