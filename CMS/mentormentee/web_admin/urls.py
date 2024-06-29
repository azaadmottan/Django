from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.index, name='web_admin_dashboard'),
    path('user-profile/', views.web_admin_profile, name='web_admin_profile'),
    path('get-profile-picture/', views.get_profile_picture, name='get_web_admin_profile_picture'),
    path('update-profile-picture/', views.update_profile_picture, name='update_web_admin_profile_picture'),
    path('get-profile-data/', views.get_profile_data, name='get_web_admin_profile_data'),
    path('user-profile-settings/', views.web_admin_profile, name='web_admin_profile_settings'),
    path('profile-security-settings/', views.web_admin_profile_settings, name='web_admin_profile_security_settings'),
    path('update-profile-info/', views.update_profile_info, name='update_web_admin_profile_info'),
    path('update-profile-location/', views.update_profile_location, name='update_web_admin_profile_location'),
    path('update-web-admin-password/', views.update_web_admin_password, name='update_web_admin_password'),
    path('mentee-users/', views.mentees, name='web_admin_mentees'),
    path('get-mentees/', views.get_mentees, name='web_admin_get_mentees'),
    path('get-mentee-profile/', views.get_mentee_profile, name='web_admin_get_mentee_profile'),
    path('mentor-users/', views.mentors, name='web_admin_mentors'),
    path("get-mentors/", views.get_mentors, name="web_admin_get_mentors"),
    path("get-mentor-profile/", views.get_mentor_profile, name="web_admin_get_mentor_profile"),
    path('mentee-queries/', views.queries, name='web_admin_queries'),
    path('get-mentee-queries/', views.get_query, name='web_admin_mentee_queries'),
    path('update-query-status/', views.update_query_status, name='web_admin_update_query_status'),
    path('delete-query/', views.delete_query, name='web_admin_delete_query'),
    path('add-notification/', views.add_notification, name='web_admin_add_notification'),
    path('get-notifications/', views.get_notifications, name='web_admin_get_notifications'),
    path('remove-notification/', views.remove_notification, name='web_admin_remove_notification'),
    path('logout_web_admin/', views.logout_user, name='logout_web_admin'),

    path('mentor-profile/<str:username>/', views.mentor_profile, name='web_admin_show_mentor_profile'),
]
