from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsCompanyOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        elif request.method not in SAFE_METHODS and request.user.role == "company":
            return True
        else:
            return False
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS or request.user.role == "admin":
            return True
        elif request.user.role == 'company':
            if obj.owner == request.user.pk:
                return True
            else:
                return False