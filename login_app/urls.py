from django.conf import settings
from django.urls import path
from . import views

from ticket_app.views.ticket_view import all_tickets

app_name = "login-app"

urlpatterns = [
    path('', views.index),
    # js only for update tabs
    path('update-tabs', views.update_tabs),
    path('register', views.register_user, name="register-user"),
    path('register-page', views.reg_page, name="register-page"),
    path('login', views.login, name="login"),
    path('signin', views.signin_page, name="login-page"),
    path('logout', views.logout, name="logout"),
    path('<int:user_id>', all_tickets, name="user-tickets"),

    path('all', views.all),

    path('<int:user_id>/level/change', views.change_user_permission_level, name="change-user-permission"),
    path('delete/<int:target_id>', views.delete_user),
    # js only for delete 
    

    path('edit/<int:user_id>', views.edit_user, name="edit-user"),
    path('new', views.new_user, name="new-user"),
]


