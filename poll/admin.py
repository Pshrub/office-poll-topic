from django.contrib import admin

# Register your models here.
from poll.models import Questions
from poll.models import Answers
from poll.models import Users
from poll.models import Votes



class AnswerInline(admin.TabularInline):
    model = Answers
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['poll_title']}),
        (None, {'fields': ['question_text']}),
        (None, {'fields': ['question_type']}),
        (None, {'fields': ['begin_date']}),
        (None, {'fields': ['end_date']}),
    ]
    inlines = [AnswerInline]
    list_display = ('poll_title','question_text', 'end_date')
    search_fields = ['question_text']

class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['email_address']}),
        (None, {'fields': ['first_name']}),
        (None, {'fields': ['last_name']}),
        (None, {'fields': ['is_active']}),
        (None, {'fields': ['is_admin']}),
    ]
    list_display = ('email_address','first_name', 'last_name')
    search_fields = ['email_address']
    
class VoteAdmin(admin.ModelAdmin):
    fieldsets = [
#        (None, {'fields': ['question_value']}),
        (None, {'fields': ['answer_value']}),
        (None, {'fields': ['voter']}),
        (None, {'fields': ['answer_timestamp']}),
    ]
    list_display = ('voter','answer_value', 'answer_timestamp')
    search_fields = ['voter']
    
    

admin.site.register(Questions, QuestionAdmin)
admin.site.register(Users, UserAdmin)
admin.site.register(Votes, VoteAdmin)
