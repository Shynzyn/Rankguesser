from django.contrib import admin
from .models import Video, Guess, Profile


class VideoAdmin(admin.ModelAdmin):
    list_display = ('ign', 'champion', 'rank', 'url',)
    list_filter = ('rank', 'ign', 'champion')
    search_fields = ('ign', 'rank', 'champion')


class GuessAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'guess', 'date_guessed')
    list_filter = ('date_guessed', 'user', 'video', 'guess')
    search_fields = ('date_guessed', 'user', 'video', 'guess')


# Register your models here.
admin.site.register(Video, VideoAdmin)
admin.site.register(Guess, GuessAdmin)
admin.site.register(Profile)
