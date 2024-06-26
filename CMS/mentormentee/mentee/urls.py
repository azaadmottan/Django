from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.index, name='mentee_dashboard'),
    path('user-profile/', views.mentee_profile, name='mentee_profile'),
    path('get-profile-picture/', views.get_profile_picture, name='get_mentee_profile_picture'),
    path('update-profile-picture/', views.update_profile_picture, name='update_mentee_profile_picture'),
    path('get-profile-data/', views.get_profile_data, name='get_mentee_profile_data'),
    path('update-profile-info/', views.update_profile_info, name='update_mentee_profile_info'),
    path('update-profile-location/', views.update_profile_location, name='update_mentee_profile_location'),
    path('mentee-query/', views.mentee_query, name='mentee_query'),
    path('add-mentee-query/', views.add_query, name='add_query'),
    path('get-mentee-query/', views.get_query, name='get_query'),
    path('logout/', views.logout_user, name='logout_mentee'),
]
