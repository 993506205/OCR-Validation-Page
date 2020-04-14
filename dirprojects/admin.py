from django.contrib import admin

from .models import DirProject
from ocrfiles.models import Ocrfiles

class OcrfilesInline(admin.TabularInline):
    model = Ocrfiles
    extra = 1

class DirProjectsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'creator_id',
                    'date', 'description',)
    list_display_links = ('id', 'name', )
    list_filter = ('name', )
    search_fields = ('name', 'creator_id')
    list_per_page = 25
    inlines = [OcrfilesInline]

admin.site.register(DirProject, DirProjectsAdmin)