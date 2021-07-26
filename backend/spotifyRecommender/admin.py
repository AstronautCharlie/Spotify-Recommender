from django.contrib import admin

# Register your models here.

from .models import Song

class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'album', 'description')

# Register your models here.

admin.site.register(Song, SongAdmin)