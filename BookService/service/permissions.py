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
