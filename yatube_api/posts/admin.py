from django.contrib import admin
from .models import Post, Comment, Group, Follow

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Group)

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'following')
    search_fields = ('user__username', 'following__username')
