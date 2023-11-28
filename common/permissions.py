from rest_framework import permissions


class IsOwnerOrAdminReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow creator of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the creator of the object, Read permissions are allowed to Admin users
        obj_user = obj.user if view.basename == "orders" else obj.order.user
        if obj_user == request.user or (request.user.is_staff and request.method in permissions.SAFE_METHODS):
            return True
