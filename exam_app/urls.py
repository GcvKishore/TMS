from django.urls import path
from . import views

app_name = "exam_app"
urlpatterns = [
    path('create-exam/', views.createExam, name="create-exam"),
    path('instructors/all-exams/', views.viewAllExamsInstructors, name="view-all-exams-instructors"),
    path('edit-exam/<int:exam_id>/', views.editExam, name="edit-exam"),
    path('edit-exam/<int:exam_id>/add-question/', views.addQuestion, name="add-question"),
    path('edit-exam/<int:exam_id>/edit-question/<int:question_id>/', views.EditQuestion, name="edit-question"),
    path('tutee/all-exams/', views.viewAllExamsTutee, name="view-all-exams-tutee"),
]
