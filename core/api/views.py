from rest_framework import viewsets, permissions
from ..models import Item
from .serializers import ItemSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Custom permission: write allowed only to owner or staff."""

    def has_object_permission(self, request, view, obj):
        # Read-only allowed
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write allowed if owner or staff
        return (obj.owner is not None and obj.owner == request.user) or request.user.is_staff


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().order_by("-created_at")
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
