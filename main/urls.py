from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_page, name='index_page'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Кастомная админка
    path('my-secret-dashboard/', views.custom_dashboard, name='custom_dashboard'),
    path('my-secret-dashboard/add-section/', views.add_section, name='add_section'),
    path('my-secret-dashboard/add-block/', views.add_block, name='add_block'),

    # Пути для редактирования и удаления (NEW)
    path('my-secret-dashboard/edit-block/<int:pk>/', views.edit_block, name='edit_block'),
    path('my-secret-dashboard/delete-block/<int:pk>/', views.delete_block, name='delete_block'),
]