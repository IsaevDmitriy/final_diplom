from rest_framework.permissions import IsAuthenticated, BasePermission


class IsAuthorPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj.creator

    def has_permission(self, request, view):
        return request.user.is_authenticated

