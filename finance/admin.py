from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, BonusRequest, Notification

# Custom User Admin
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'phone', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email', 'phone')

# BonusRequest Admin
@admin.register(BonusRequest)
class BonusRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'amount', 'created_by', 'assigned_to', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('title', 'reason')
    raw_id_fields = ('created_by', 'assigned_to')
    date_hierarchy = 'created_at'

# Notification Admin
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at', 'bonus_request')
    list_filter = ('is_read', 'created_at')
    search_fields = ('message',)
    raw_id_fields = ('user', 'bonus_request')
