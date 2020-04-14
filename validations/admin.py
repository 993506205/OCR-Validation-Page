from django.contrib import admin

from .models import Validation


class ValidationAdmin(admin.ModelAdmin):
    list_display = ('id', 'ocrfiles', 'page_number', 'get_text', 'is_correct',
                    'feedback_text', 'correction_rate')
    list_display_links = ('id', 'ocrfiles', 'page_number', 'get_text')
    list_filter = ('ocrfiles',)
    search_fields = ('ocrfiles', 'get_text', 'feedback_text')
    list_per_page = 25


admin.site.register(Validation, ValidationAdmin)
