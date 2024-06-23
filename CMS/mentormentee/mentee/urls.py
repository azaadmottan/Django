from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.index, name='mentee_dashboard'),
    path('mentee-query/', views.mentee_query, name='mentee_query'),
    path('add-mentee-query/', views.add_query, name='add_query'),
    path('get-mentee-query/', views.get_query, name='get_query'),
    path('logout/', views.logout_user, name='logout_mentee'),
]
