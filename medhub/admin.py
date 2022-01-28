from django.contrib import admin
from medhub.models import Responder, Interrogator, Poll, Question, Answer


admin.site.register(Interrogator)
admin.site.register(Responder)
admin.site.register(Poll)
admin.site.register(Question)
admin.site.register(Answer)