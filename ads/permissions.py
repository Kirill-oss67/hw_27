from rest_framework import permissions

from ads.models import Selection, User


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


# class SelectionCreatePermissions(permissions.BasePermission):
#     message = "you can't create permission"
#
#     def has_permission(self, request, view):
#         if view.kwargs['owner'] == request.user.id:
#             return True
#         elif request.user.role != User.Role.MEMBER:
#             return True
#         else:
#             return False
