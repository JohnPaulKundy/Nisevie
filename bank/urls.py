from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import login_view, home_view, registration_view, plan_manager_view, plan_list_view, send_funds_view

urlpatterns = [
    path('registration/', registration_view, name='registration'),
    path('', login_view, name='login'),
    path('home/', home_view, name='home'),
    path('plan_list/', plan_list_view, name='plan_list'),
    path('plan_manager/', plan_manager_view, name='plan_manager'),
    path('send_fund/', send_funds_view, name='send_fund'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
