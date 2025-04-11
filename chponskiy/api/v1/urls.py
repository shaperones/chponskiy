from django.urls import path

from chponskiy.api.v1 import views

urlpatterns = [
    path('game/<slug:slug>/', views.game, name='game'),
    path('question/<slug:slug>', views.question, name='question'),
    path('upload_score', views.upload_score, name='upload_score'),
]
