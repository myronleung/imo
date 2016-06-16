from django.contrib import admin

from .models import Choice, Question, UserProfile, Comment, Friendship, Feedback, Voted

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]
    list_filter = ["pub_date", 'category']
    list_display = ["question_text", 'pub_date', 'total_votes']

class FeedbackAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['topic']}),
        ('feedback',        {'fields': ['feedback', 'agree']})
    ]
    list_filter = ['pub_date']
    list_display = ['topic', 'agree', 'pub_date']
class UserProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['name']}),
        ('sponsor',          {'fields': ['sponsor']}),
        ('information',      {'fields': ['gender', 'birthday', 'picture', 'about', 'motto']}),
        ('activity',         {'fields': ['total_friends', 'inappropriate']})
    ]
    list_filter = ['sponsor', 'join_date']
    list_display = ['name', 'inappropriate', 'join_date']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
