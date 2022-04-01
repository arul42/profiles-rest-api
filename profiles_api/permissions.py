from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Allow user to update theire own profile"""

    def has_object_permission(self, request, view, obj):
        """check user is trying to update theire own profile"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id


class UpdateOwnStatus(permissions.BasePermission):
    """Allow users to update theire own profile"""

    def has_object_permission(self, request, view, obj):
        """Check post owner"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user_profile.id == request.user.id
