from django.urls import path
from .views import article_list, article_details, user_login, register, user_logout, article_form, update_article, delete_article, password_change, password_change_done
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView

urlpatterns = [
    path('', article_list, name='article_list'),
    path('articles/<slug:slug>', article_details, name='article_details'),
    # path('login/', user_login, name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
    path('password-change/', password_change, name='password_change'),
    path('password-change-done/', password_change_done, name='password_change_done'),
    path('add/', article_form, name='article_form'),
    path('update/<slug:slug>', update_article, name='update_article'),
    path('delete/<slug:slug>', delete_article, name='delete_article'),
]
