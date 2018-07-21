
from django.contrib import admin
from django.urls import path
#from django.conf.urls import include, url
from forum.views import *
from forum.views.ques import *
urlpatterns = [
# path('addcom/<int:id>/',CreateCommentView.as_view(),name='add_comm_html'),
    path("signup/", SignupController.as_view(), name='signup'),
    path("login/", LoginController.as_view(), name='login'),
    path("logout/",logout_view,name='logout'),
    path('questions/',QuestionsListView.as_view(),name='questions_html'),
    path('question/<int:id>/',CreateCommentView.as_view(),name='question_details_html'),
    path("addque/",CreateQuestionView.as_view(),name='add_que_html'),
    path("myquestions/",MyQuestionsListView.as_view(),name='myques_html'),
    path('que/update/<int:id>/',UpdateQuestionView.as_view(),name='edit_ques'),
    path('que/delete/<int:id>/',DeleteQuestionView.as_view(),name='delete_ques'),
    path('que/comment/<int:id>/',DeleteCommentView.as_view(),name='delete_comm'),
    path('tags/',TagsListView.as_view(),name='tags_html'),
    path('tags/<str:tag>/',TagsDetailListView.as_view(),name='tags_details_html'),
]
