from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.index, name='mentor_dashboard'),
    path('logout/', views.logout_user, name='logout_mentor'),
    path('mentee-users/', views.mentee, name='mentee_users'),
    path('mentee-queries/', views.query, name='mentee_queries'),
]
