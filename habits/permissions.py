from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    Message = "Вы не владелец"

    def has_object_permission(self, request, view, obj):
        if request.user == obj.author:
            return True
        return False


class IsPublic(BasePermission):
    message = "У вас нет доступа к публичным привычкам"

    def has_object_permission(self, request, view, obj):
        if obj.is_public:
            return True
        return False
