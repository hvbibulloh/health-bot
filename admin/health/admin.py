from django.contrib import admin
from .models import User, Vakansiya, VakansiyaRU


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'full_name', 'city', 'created_at')
    search_fields = ('phone_number', 'city', 'full_name', 'created_at')
    list_filter = ( 'city', 'created_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


@admin.register(Vakansiya)
class VakansiyaAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_at')
    search_fields = ('name', 'status', 'created_at')
    list_filter = ('name', 'status', 'created_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


@admin.register(VakansiyaRU)
class VakansiyaAdminRu(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_at')
    search_fields = ('name', 'status', 'created_at')
    list_filter = ('name', 'status', 'created_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
