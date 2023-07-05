from django.shortcuts import render
from .models import Post
from .models import Comment
from .serializers import *
from rest_framework import viewsets

# APIView를 사용하기 위해 import
# from rest_framework import mixins
# from rest_framework import generics
# from django.http import JsonResponse
from django.shortcuts import get_object_or_404
# from django.views.decorators.http import require_http_methods
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from django.http import Http404

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import permissions

# DRF는 FBV보다 CBV 선호
# APIView > Mixins > Generic CBV > ViewSet

########### viewset ############
# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

# class CommentViewSet(viewsets.ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, post):
        if request.method in permissions.SAFE_METHODS:
            return True
        return post.writer == request.user

class PostList(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def post(self, request, format=None):
        request.data['writer'] = request.user.id
        # 장고가 bearer token을 자동으로 인식하고 request에 넣어주도록 한다.
        serializer = PostSerializer(data=request.data) # 시리얼라이징
        if serializer.is_valid(): # 유효성 검사

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True) # 많은 post들을 받아오려면 (many=True) 써줘야 한다! 이렇게 에러뜨는 경우가 생각보다 많다.
        return Response(serializer.data)
    

    # 수정 / 삭제 모두 할 수 있어야 하므로 put과 delete를 구현
    def put(self,request):
        id = request.data.id
        request.data['writer'] = request.user.id
        post = get_object_or_404(Post, id=id)
        self.check_object_permissions(request, post)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request):
        id = request.data.get('id')
        request.data['writer'] = request.user.id
        post = get_object_or_404(Post, id=id)
        self.check_object_permissions(request, post)
        post.delete()
        return Response(data="Deleted Successfully",status=status.HTTP_202_ACCEPTED)




class CommentList(APIView):
    def post(self, request, format=None):
        serializer = CommentSerializer(data=request.data) # 시리얼라이징
        if serializer.is_valid(): # 유효성 검사
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, format=None):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True) # 많은 comment들을 받아오려면 (many=True) 써줘야 한다! 이렇게 에러뜨는 경우가 생각보다 많다.
        return Response(serializer.data)

class PostDetail(APIView):
    def get(self,request,id):
        post = get_object_or_404(Post, id=id)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    def put(self,request,id):
        post = get_object_or_404(Post, id=id)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,id):
        post = get_object_or_404(Post, id=id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class CommentDetail(APIView):
    def get(self,request,id):
        comment = get_object_or_404(Comment, id=id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    
    def put(self,request,id):
        comment = get_object_or_404(Comment, id=id)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,id):
        post = get_object_or_404(Comment, id=id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




###################################
######### DEPRECATED CODE #########
###################################


## MIXINS ##

# class PostListMixins(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request)
        
#     def post(self, request, *args, **kwargs):
#         return self.create(request,*args,**kwargs)
    
# class PostDetailMixins(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request,*args,**kwargs)
    
#     def put(self, request, *args, **kwargs):
#         return self.update(request,*args,**kwargs)
    
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request,*args,**kwargs)


## genericAPIview ##

# class PostListGenericAPIView(generics.ListCreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

# class PostDetailGenericAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer




## API VIEW ##

# post_list = PostViewSet.as_view({
#     'get' : 'list',
#     'post' : 'create',
# })

# post_detail_vs = PostViewSet.as_view({
#     'get' : 'retrieve',
#     'put' : 'update',
#     'patch' : 'partial_update',
#     'delete' : 'destroy',
# })



# postList와 postDetail이 있을 때, post생성은 어디에 들어가야할까?
# postList에 넣는 것이 일반적, 하나만 올리는 거니까 detail아닌가? 하지만 List가 일반적이라고 한다.

# @require_http_methods(["GET", "PATCH", "DELETE"])
# def post_detail(request, id):
#     if request.method == "GET":
#         post = get_object_or_404(Post, pk = id)
#         category_json ={
#             "writer" : post.writer,
#             "content" : post.content,
#             "category" : post.category,
#         }
#         # id는 autoField기 때문에 오류
#         return JsonResponse({
#             'status' : 200,
#             'message' : '게시글 조회 성공',
#             'data' : category_json
#         })
#     elif request.method == "PATCH":
#         body = json.loads(request.body.decode('utf-8'))
#         update_post = get_object_or_404(Post, pk=id)

#         update_post.content = body['content']
#         update_post.category = body['category']
#         update_post.save()
#         update_post_json = {
#             "id" : update_post.id,
#             "writer" : update_post.writer,
#             "content" : update_post.content,
#             "category" : update_post.category,
#         }

#         return JsonResponse({
#             'status' : 200,
#             'message' : '게시글 조회 성공',
#             'data' : update_post_json
#         })
#     elif request.method == "DELETE":
#         body = json.loads(request.body.decode('utf-8'))
#         delete_post = get_object_or_404(Post, pk=id)
#         delete_post.delete()
#         return JsonResponse({
#             'status' : 200,
#             'message' : '게시글 삭제 성공'
#         })

# def get_all_posts(request):
#     found = True
#     data = []
#     id=1
#     while True:
#         try:
#             post = get_object_or_404(Post, pk = id)
#             category_json ={
#                 "id" : id,
#                 "writer" : post.writer,
#                 "content" : post.content,
#                 "category" : post.category,
#             }
#             data.append(category_json)
#             id+=1
#         except:
#             found = False
#         if found == False:
#             break

#     return JsonResponse({
#         'status' : 200,
#         'message' : '모든 게시글 조회 성공',
#         'data' : data
#     })
# #전부 불러오는 함수 만들어야 하니 다 반복문으로 전부 json request하고 try except로 404 뜰때 멈추면 될듯?

# @require_http_methods(["POST"])
# def createPost(request):
#     body = json.loads(request.body.decode('utf-8'))
#     newPost = Post.objects.create(
#         writer = body['writer'],
#         content = body['content'],
#         category = body['category']
#     )

#     newPostJson = {
#         "id": newPost.id,
#         "writer": newPost.writer,
#         "category": newPost.category
#     }

#     return JsonResponse({
#         'status' : 200,
#         'message' : 'Success',
#         'data' : newPostJson,
#     })

# @require_http_methods(["GET"])
# def get_comment(request, id):
#     comment_all = Comment.objects.filter(post = id)
#     comment_json_list = []
#     for comment in comment_all:
#         comment_json = {
#             'writer': comment.writer,
#             'content': comment.content
#         }
#         comment_json_list.append(comment_json)
#     return JsonResponse({
#         'status' : 200,
#         'message' : '댓글 읽기 성공',
#         'data' : comment_json_list
#     })

# @require_http_methods(["POST"])
# def uploadComment(request, id):
#     targetPost = get_object_or_404(Post, pk = id)
#     body = json.loads(request.body.decode('utf-8'))
#     newComment = Comment.objects.create(
#         writer = body['writer'],
#         content = body['content'],
#         post = targetPost
#     )
#     return JsonResponse({
#         'status' : 200,
#         'message' : '댓글 달기 성공',
#         'data' : {
#             'writer' : newComment.writer,
#             'content' : newComment.content,
#             'id' : id
#         }
#     })


# def getPostsBefore(request, inputDate):
#     # 연도를 안썼으면 올해로, 두자리면 썼으면 앞에 붙여서"
#     if len(inputDate) == 4:
#         today = datetime.date.today()
#         year = str(today.year)
#         month = inputDate[0:2]
#         day = inputDate[2:4]
#     elif len(inputDate) == 6:
#         year = str(20) + inputDate[0:2]
#         month = inputDate[2:4]
#         day = inputDate[4:6]
#     elif len(inputDate) == 8:
#         year = inputDate[0:4]
#         month = inputDate[4:6]
#         day = inputDate[6:8]
#     else:
#         return JsonResponse({
#         'status': 500,
#         'message':'invalid date digit'
#     })

#     if int(year)>2050 or int(year)<1950 or int(month)>12 or int(day)>30:
#          return JsonResponse({
#         'status': 500,
#         'message':'invalid date format'
#     })

#     year = int(year)
#     month = int(month)
#     day = int(day)
#     filteredPosts = Post.objects.filter(created_at__range = (datetime.date(2023, 4, 5),datetime.date(year,month,day)))
#     filteredPosts_list = []
#     for obj in filteredPosts:
#         filteredPosts_list.append({
#             "id" : obj.id,
#             "writer" : obj.writer,
#             "content" : obj.content,
#             "category" : obj.category
#         })
#     return JsonResponse({
#         'status':200,
#         'message':'Success',
#         'data': filteredPosts_list
#     })

# def get_all_posts(resquest):
#     found = True
#     data = []
#     id=1
#     while True:
#         try:
#             post = get_object_or_404(Post, pk = id)
#             category_json ={
#                 "id" : id,
#                 "writer" : post.writer,
#                 "content" : post.content,
#                 "category" : post.category,
#             }
#             data.append(category_json)
#             id+=1
#         except:
#             found = False
#         if found == False:
#             break

#     return JsonResponse({
#         'status' : 200,
#         'message' : '모든 게시글 조회 성공',
#         'data' : data
#     })
# #전부 불러오는 함수 만들어야 하니 다 반복문으로 전부 json request하고 try except로 404 뜰때 멈추면 될듯?