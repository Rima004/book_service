from rest_framework import permissions

class CheckRole(permissions.BasePermission):

    EDIT_METHODS = ['PUT', 'PATCH', 'DELETE']

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method == 'POST':
            print (request.method+" "+request.user.role)
            return request.user.role == 'provider'

        return True

    def has_object_permission(self, request, view, obj):
        if request.method in self.EDIT_METHODS:
            return (
                request.user.role == 'provider' and
                obj.provider == request.user
            )
        return True

class PermissionsForBooking(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.method == 'POST':
            return request.user.role == 'client'
        if request.method == 'GET':
            return request.user.role in ['client', 'provider']

        return True

    def has_object_permission(self, request, view, obj):

        if request.method == 'PATCH' :
            return (
                request.user.role == 'provider'
                and obj.service.provider == request.user
            )

        return True


class WorkSchedulePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
                request.user.is_authenticated
                and request.user.role == 'provider'
        )

    def has_object_permission(self, request, view, obj):

         return (request.user.role == 'provider'
                 and obj.provider == request.user)



