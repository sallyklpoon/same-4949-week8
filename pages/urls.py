# pages/urls.py
from django.urls import path
from .views import homePageView, aboutPageView, sallyPageView, homePost, results

urlpatterns = [
    path('', homePageView, name='home'),
    path('about/', aboutPageView, name='about'),
    path('sally/', sallyPageView, name='sally'),
    path('homePost/', homePost, name='homePost'),
    path('results/<int:choice>/<str:gmat>/', results, name='results'),
]
