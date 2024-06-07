from rest_framework.permissions import BasePermission


class IsOwnerOrModerator(BasePermission):

    def has_permission(self, request, view):
        if request.user.groups.filter(name="Moderator").exists():
            return True

        return request.user == view.get_object().owner


class IsNotModerator(BasePermission):

    def has_permission(self, request, view):
        if request.user.groups.filter(name="Moderator").exists():
            return False

        return True


class IsOwner(BasePermission):

    def has_permission(self, request, view):
        return request.user == view.get_object().owner
