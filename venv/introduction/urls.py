from django.urls import path
from introduction.views import *

urlpatterns = [
    path('', sendIntroduction, name='sendIntroduction'),
]