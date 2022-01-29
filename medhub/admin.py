from django.contrib import admin
from medhub.models import Responder, Interrogator, Poll, Question, Answer


# admin.site.register(Interrogator)
# admin.site.register(Responder)
# admin.site.register(Poll)
# admin.site.register(Question)
# admin.site.register(Answer)


@admin.register(Interrogator)
class InterrogatorAdmin(admin.ModelAdmin):
	search_fields = ('username', )
	list_display =  'username', 'full_name', 'password'


@admin.register(Responder)
class ResponderAdmin(admin.ModelAdmin):
	search_fields = ('birth_date', 'gender')
	list_display = 'gender', 'birth_date'


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
	search_fields = ('name',)
	list_display = 'name', 'created'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
	search_fields = ('main_question',)
	list_display = 'main_question', 'sub_question'


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
	search_fields = ('responder', 'poll')
	list_display = 'responder', 'poll', 'interrogator', 'main_answer'