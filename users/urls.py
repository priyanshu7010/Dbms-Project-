from django.urls import path, re_path
from users import views

urlpatterns = [
    path('', views.home_view, name='home'),
    
    # Insert user
    re_path(r'^Insertuser/?$', views.insert_user_view, name='insert_user'),
    re_path(r'^insertuser/?$', views.insert_user_view, name='insert_user_lower'),
    
    # Show user
    re_path(r'^showuser/?$', views.show_user_view, name='show_user'),
    
    # Sort user
    re_path(r'^sortuser/?$', views.sort_user_view, name='sort_user'),
    
    # Edit / Update user
    re_path(r'^edituser/(?P<user_id>\d+)/?$', views.edit_user_view, name='edit_user'),
    re_path(r'^updateuser/(?P<user_id>\d+)/?$', views.update_user_view, name='update_user'),
    
    # Delete user
    re_path(r'^Deluser/(?P<user_id>\d+)/?$', views.delete_user_view, name='delete_user'),
    re_path(r'^deluser/(?P<user_id>\d+)/?$', views.delete_user_view, name='delete_user_lower'),
    
    # Query pages
    re_path(r'^runQueryuser/?$', views.run_query_user_view, name='run_query_user'),
    re_path(r'^ProcessCustomQuery/?$', views.process_custom_query_view, name='process_custom_query'),
    
    # CSV export
    re_path(r'^export_csv/?$', views.export_csv_view, name='export_csv'),
]
