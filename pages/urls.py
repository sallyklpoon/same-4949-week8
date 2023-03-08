# pages/urls.py
from django.urls import path
from .views import homePageView, aboutPageView, sallyPageView, \
    homePost, results, todos, register, message

urlpatterns = [
    path('', homePageView, name='home'),
    path('about/', aboutPageView, name='about'),
    path('sally/', sallyPageView, name='sally'),
    path('homePost/', homePost, name='homePost'),
    path('results/<int:choice>/<str:gmat>/', results, name='results'),
    path('todos', todos, name='todos'),
    path("register/", register, name="register"),
    path("message/<str:msg>/<str:title>", message, name="message"),
]
