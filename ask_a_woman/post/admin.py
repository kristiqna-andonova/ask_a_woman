from django.contrib import admin

from ask_a_woman.post.models import Post


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass