from django.urls import path
from introduction.views import *

urlpatterns = [
    path('introduction', sendIntroduction, name='sendIntroduction'),
]