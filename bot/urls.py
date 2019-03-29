from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:groupme_bot_id>/', views.bot, name='bot'),
]