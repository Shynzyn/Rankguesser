from django.contrib import admin
from .models import Video, Guess


class VideoAdmin(admin.ModelAdmin):
    list_display = ('ign', 'rank', 'url')
    list_filter = ('rank', 'ign')
    search_fields = ('ign', 'rank')


# Register your models here.
admin.site.register(Video, VideoAdmin)
admin.site.register(Guess)
