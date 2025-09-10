from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrOwnerOrReadOnly(BasePermission):
def has_object_permission(self, request, view, obj):
if request.method in SAFE_METHODS:
return True
user = request.user
# Admin can edit; owner of product can edit
return getattr(user, 'role', None) == 'ADMIN' or getattr(obj, 'owner_id', None) == user.id