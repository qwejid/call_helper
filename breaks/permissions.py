from rest_framework.permissions import IsAuthenticated

class IsMyReplacementManager(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if obj.group.organisation.director == request.user:
            return True
        if request.group.manager.user == request.user:
            return True
        return False