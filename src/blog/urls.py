from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.topic_list, name='topic_list'),
    path('search/', views.topic_search, name='topic_search'),
    path('topic/<int:topic_id>/', views.topic_detail, name='topic_detail'),
    path('health/', views.health_check, name='health_check'),
]
