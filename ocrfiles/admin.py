from django.contrib import admin

from .models import Ocrfiles, OcrConvertedImage


class OcrConvertedImageInline(admin.TabularInline):
    model = OcrConvertedImage
    extra = 1


class OcrfilesAdmin(admin.ModelAdmin):
    list_display = ('id', 'file_name', 'upload_date',
                    'file_size', 'file_extension')
    list_display_links = ('id', 'file_name', )
    list_filter = ('file_extension', )
    search_fields = ('file_name', 'file_extension')
    list_per_page = 25
    inlines = [OcrConvertedImageInline]


admin.site.register(Ocrfiles, OcrfilesAdmin)
