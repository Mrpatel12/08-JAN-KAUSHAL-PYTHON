from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('users/', views.user_list, name='admin_user_list'),
    path('users/add/', views.add_user, name='admin_add_user'),
    path('users/<int:pk>/edit/', views.edit_user, name='admin_edit_user'),
    path('users/<int:pk>/delete/', views.delete_user, name='admin_delete_user'),
    path('users/<int:pk>/toggle-status/', views.toggle_user_status, name='admin_toggle_user_status'),
    path('notes/', views.admin_note_list, name='admin_note_list'),
    path('notes/<int:pk>/delete/', views.admin_delete_note, name='admin_delete_note'),
]
