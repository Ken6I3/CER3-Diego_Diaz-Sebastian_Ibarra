from rest_framework.permissions import BasePermission, SAFE_METHODS

class Admin_o_JV(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        
        if user.is_staff:
            return True
        
        en_junta = user.groups.filter(name='Junta de vecinos').exists()

        if en_junta and request.method in SAFE_METHODS + ('POST',):
            return True

        return False