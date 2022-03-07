from django.urls import path
from . import views
urlpatterns = [
    path('questions/', views.questions, name='questions'),
    path('question/<str:pk>/', views.question, name='question-detail'),
    path('welcome/', views.first_page, name='welcome'),
    path('login/', views.loginuser, name='login'),
    path('register/', views.registeruser, name='register'),
    path('logout/', views.logoutuser, name='logout'),
    path('table/', views.table, name='table'),
    path('create-team/', views.create_team, name='create-team'),
    path('join-team/', views.join_team, name='join-team'),
    path('', views.redirect_view, name='')



]
