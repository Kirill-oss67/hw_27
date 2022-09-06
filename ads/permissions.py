from rest_framework import permissions

from ads.models import Selection, User, Ad


class SelectionUpdatePermissions(permissions.BasePermission):
    message = "you can't touch this permissions"

    def has_permission(self, request, view):
        try:
            selection = Selection.objects.get(pk=view.kwargs['pk'])
        except Selection.DoesNotExist:
            return False
        if selection.owner.id == request.user.id:
            return True
        elif request.user.role != User.Role.MEMBER:
            return True
        else:
            return False

class AdUpdateDeletePermission(permissions.BasePermission):
    message = "you can't update it without some permissions"

    def has_permission(self, request, view):
        try:
            ad = Ad.objects.get(pk=view.kwargs['pk'])
        except Ad.DoesNotExist:
            return False
        if ad.author.id == request.user.id:
            return True
        elif request.user.role != User.Role.MEMBER:
            return True
        else:
            return False

