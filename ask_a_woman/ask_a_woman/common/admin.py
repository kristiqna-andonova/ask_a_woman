from django.contrib import admin

from ask_a_woman.common.models import Like, Comment, Bookmark


# Register your models here.
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

@admin.register(Bookmark)
class ModelNameAdmin(admin.ModelAdmin):
    pass