from django.urls import include, path
from posts.views import *
from rest_framework.routers import DefaultRouter

# urlpatterns = [
#     # path('', hello_world, name='hello_world'),

#     # path('all', get_all_posts, name='get_all_posts'),
#     # path('<int:id>/', post_detail, name='post_detail'),
#     # path('new/', createPost, name='createPost'),
#     # path('comment/<int:post_id>/', get_comment, name='get_comment'),
#     # path('newcomment/<int:post_id>/', uploadComment, name='uploadComment'),
#     # path('createdbefore/<str:inputDate>/', getPostsBefore, name='getPostsBefore'),
#     # path('post_detail', get_all_posts, name='get_all_posts'),
#     # path('post_detail/<int:id>', post_detail, name='get_post_detail'),

#     path('', post_list),
#     path('<int:pk>/', post_detail_vs),

        
#     # path('', PostList.as_view(), name='PostList'),
#     # path('<int:id>/', PostDetail.as_view(), name=''),
#     # path('comment', CommentList.as_view(), name='CommentList'),
#     # path('commment/<int:id>/', CommentDetail.as_view(), name=''),


#     # GENERIC API VIEW    
#     # path('', PostListGenericAPIView.as_view(), name='PostList'),
#     # path('<int:pk>/', PostDetailGenericAPIView.as_view(), name='PostDetail'),
# ]
# <int:pk> 는 int 값을 받고 그걸 pk에 넘긴다는 뜻

router = DefaultRouter()
router.register('', PostViewSet)
router.register('comment', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]