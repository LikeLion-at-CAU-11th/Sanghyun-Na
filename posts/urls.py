from django.urls import path
from posts.views import *

urlpatterns = [
    path('', hello_world, name='hello_world'),
    path('all', get_all_posts, name='get_all_posts'),
    path('<int:id>/', post_detail, name='post_detail'),
    path('new/', createPost, name='createPost'),
    path('comment/<int:post_id>/', get_comment, name='get_comment'),
    path('newcomment/<int:post_id>/', uploadComment, name='uploadComment'),
    path('createdbefore/<str:inputDate>/', getPostsBefore, name='getPostsBefore'),
]
# <int:pk> 는 int 값을 받고 그걸 pk에 넘긴다는 뜻