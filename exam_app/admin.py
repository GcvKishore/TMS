from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(MakeExam)
admin.site.register(MakeQuestion)
admin.site.register(Option)
admin.site.register(Answer)
admin.site.register(UserResults)
admin.site.register(UserExamDetails)
admin.site.register(UserQuestionDetails)
admin.site.register(UserAnswerTextInput)
admin.site.register(UserAnswerFileUpload)
