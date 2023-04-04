from django.urls import path
from posts.views import *

urlpatterns = [
    path('', hello_world, name='hello_world'),
    path('post_detail/<int:id>', get_post_detail, name='get_post_detail'),
]
# <int:pk> 는 int 값을 받고 그걸 pk에 넘긴다는 뜻