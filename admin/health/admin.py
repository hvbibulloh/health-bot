from django.contrib import admin

from .models import User, Vakansiya, VakansiyaRU, Media, BizHaqimizda, BizHaqimizdaRu, Taklif


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'full_name', 'city', 'created_at', 'ball')
    search_fields = ('phone_number', 'city', 'full_name', 'created_at')
    list_filter = ('city', 'created_at')
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


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('name', 'media', 'created_at', 'status')
    ordering = ('-created_at',)


@admin.register(BizHaqimizda)
class BizHaqimizdaAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    ordering = ('-created_at',)


@admin.register(BizHaqimizdaRu)
class BizHaqimizdaRuAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    ordering = ('-created_at',)


@admin.register(Taklif)
class TaklifAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'created_at')
    ordering = ('-created_at',)
