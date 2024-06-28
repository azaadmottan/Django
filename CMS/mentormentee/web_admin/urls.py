from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.index, name='web_admin_dashboard'),
    path('user-profile/', views.web_admin_profile, name='web_admin_profile'),
    path('get-profile-data/', views.get_profile_data, name='get_web_admin_profile_data'),
    path('user-profile-settings/', views.web_admin_profile, name='web_admin_profile_settings'),
    path('update-password/', views.web_admin_profile_settings, name='web_admin_password'),

    path('mentee-users/', views.mentees, name='web_admin_mentees'),
    path('mentor-users/', views.mentors, name='web_admin_mentors'),
    path("get-mentors/", views.get_mentors, name="web_admin_get_mentors"),
    path("get-mentor-profile/", views.get_mentor_profile, name="web_admin_get_mentor_profile"),

    path('mentee-queries/', views.queries, name='web_admin_queries'),

    path('logout_web_admin/', views.logout_user, name='logout_web_admin'),
]
