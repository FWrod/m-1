from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('login/', views.login),
    path('cadastrar/', views.register),
    path('carta/<str:title>/', views.card),
    path('deck/<str:title>/', views.deck),
    path('<str:username>/', views.profile),
    path('django/admin/', admin.site.urls),
]

handler404 = views.error404
handler500 = views.error500