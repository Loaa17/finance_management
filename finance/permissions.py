from rest_framework import permissions

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'MANAGER'

class IsFinanceStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'FINANCE'