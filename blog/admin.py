from django.contrib import admin

from .models import Post, ContactMessage

admin.site.register(Post)
admin.site.register(ContactMessage)
