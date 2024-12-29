from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('query/', views.query, name='query'),
    path('forgot/', views.forgot, name='forgot'),
    path('signup/', views.signup, name='signup'),
    path('heatmap/', views.heatmap, name='heatmap'),
    path('vaccine-baby/', views.babyVaccination, name='babyVaccination'),
    path('vaccine-general/', views.generalVaccination, name='generalVaccination'),
    path('profile/', views.profile, name='profile'),
    path('precaution/', views.precaution, name='precaution'),
    path('online-meet/', views.virtualMeet, name='virtualMeet'),
    path('ticket/', views.ticket, name='ticket'),
]