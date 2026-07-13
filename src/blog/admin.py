from django.contrib import admin
from .models import Topic, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('TopicID', 'TopicName', 'TopicPublishingDate')
    search_fields = ('TopicName', 'TopicDescription')
    list_filter = ('TopicPublishingDate',)
    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('CommentNumber', 'CommenterName', 'TopicID')
    search_fields = ('CommenterName', 'CommentText')
    list_filter = ('TopicID',)
