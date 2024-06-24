from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.index, name='mentor_dashboard'),
    path('logout/', views.logout_user, name='logout_mentor'),
    path('mentee-users/', views.mentee, name='mentee_users'),
    path('get-mentee-profile/', views.get_mentee_profile, name='get_mentee_profile'),
    path('get-mentees-of-mentor/', views.get_mentees_of_mentor, name='get_mentees_of_mentor'),
    path('get-unassigned-mentees/', views.get_unassigned_mentees, name='get_unassigned_mentees'),
    path('add-mentee/', views.add_mentee, name='add_mentee'),
    path('remove-mentee/', views.remove_mentee, name='remove_mentee'),
    path('mentee-queries/', views.query, name='mentee_queries'),
    path('get-mentee-queries/', views.get_query, name='get_mentee_queries'),
    path('update-query-status/', views.update_query_status, name='update_query_status'),
]
