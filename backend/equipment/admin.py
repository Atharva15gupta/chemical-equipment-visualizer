from django.contrib import admin
from .models import Dataset


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ['filename', 'user', 'uploaded_at', 'total_count']
    list_filter = ['uploaded_at', 'user']
    search_fields = ['filename', 'user__username']
    readonly_fields = ['uploaded_at']
