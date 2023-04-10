from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import Post
from .models import Comment


import json
import datetime
# Create your views here.

def hello_world(request):
    if request.method == "GET":
        return JsonResponse({
            "status" : 200,
            "success" : True,
            "message" : "Message delivered!",
            "data" : "Hello World!",
        })
    
@require_http_methods(["GET", "PATCH", "DELETE"])
def post_detail(request, id):
    if request.method == "GET":
        post = get_object_or_404(Post, pk = id)
        category_json ={
            "writer" : post.writer,
            "content" : post.content,
            "category" : post.category,
        }
        # id는 autoField기 때문에 오류
        return JsonResponse({
            'status' : 200,
            'message' : '게시글 조회 성공',
            'data' : category_json
        })
    elif request.method == "PATCH":
        body = json.loads(request.body.decode('utf-8'))
        update_post = get_object_or_404(Post, pk=id)

        update_post.content = body['content']
        update_post.category = body['category']
        update_post.save()
        update_post_json = {
            "id" : update_post.post_id,
            "writer" : update_post.writer,
            "content" : update_post.content,
            "category" : update_post.category,
        }

        return JsonResponse({
            'status' : 200,
            'message' : '게시글 조회 성공',
            'data' : update_post_json
        })
    elif request.method == "DELETE":
        body = json.loads(request.body.decode('utf-8'))
        delete_post = get_object_or_404(Post, pk=id)
        delete_post.delete()
        return JsonResponse({
            'status' : 200,
            'message' : '게시글 삭제 성공'
        })

def get_all_posts(request):
    found = True
    data = []
    id=1
    while True:
        try:
            post = get_object_or_404(Post, pk = id)
            category_json ={
                "id" : id,
                "writer" : post.writer,
                "content" : post.content,
                "category" : post.category,
            }
            data.append(category_json)
            id+=1
        except:
            found = False
        if found == False:
            break

    return JsonResponse({
        'status' : 200,
        'message' : '모든 게시글 조회 성공',
        'data' : data
    })
#전부 불러오는 함수 만들어야 하니 다 반복문으로 전부 json request하고 try except로 404 뜰때 멈추면 될듯?

@require_http_methods(["POST"])
def createPost(request):
    body = json.loads(request.body.decode('utf-8'))
    newPost = Post.objects.create(
        writer = body['writer'],
        content = body['content'],
        category = body['category']
    )

    newPostJson = {
        "id": newPost.post_id,
        "writer": newPost.writer,
        "category": newPost.category
    }

    return JsonResponse({
        'status' : 200,
        'message' : 'Success',
        'data' : newPostJson,
    })

@require_http_methods(["GET"])
def get_comment(request, post_id):
    comment_all = Comment.objects.filter(post = post_id)
    comment_json_list = []
    for comment in comment_all:
        comment_json = {
            'writer': comment.writer,
            'content': comment.content
        }
        comment_json_list.append(comment_json)
    return JsonResponse({
        'status' : 200,
        'message' : '댓글 읽기 성공',
        'data' : comment_json_list
    })

@require_http_methods(["POST"])
def uploadComment(request, post_id):
    targetPost = get_object_or_404(Post, pk = post_id)
    body = json.loads(request.body.decode('utf-8'))
    newComment = Comment.objects.create(
        writer = body['writer'],
        content = body['content'],
        post = targetPost
    )
    return JsonResponse({
        'status' : 200,
        'message' : '댓글 달기 성공',
        'data' : {
            'writer' : newComment.writer,
            'content' : newComment.content,
            'post_id' : post_id
        }
    })

# def isNewer(a,b){
        
# }

# def isBetweenDates(start, end, middle):


def getPostsBefore(request, inputDate):
    # 연도를 안썼으면 올해로, 두자리면 썼으면 앞에 붙여서"
    if len(inputDate) == 4:
        today = datetime.date.today()
        year = str(today.year)
        month = inputDate[0:2]
        day = inputDate[2:4]
    elif len(inputDate) == 6:
        year = str(20) + inputDate[0:2]
        month = inputDate[2:4]
        day = inputDate[4:6]
    elif len(inputDate) == 8:
        year = inputDate[0:4]
        month = inputDate[4:6]
        day = inputDate[6:8]
    else:
        return JsonResponse({
        'status': 500,
        'message':'invalid date digit'
    })

    if int(year)>2050 or int(year)<1950 or int(month)>12 or int(day)>30:
         return JsonResponse({
        'status': 500,
        'message':'invalid date format'
    })

    year = int(year)
    month = int(month)
    day = int(day)
    filteredPosts = Post.objects.filter(created_at__range = (datetime.date(2023, 4, 5),datetime.date(year,month,day)))
    filteredPosts_list = []
    for obj in filteredPosts:
        filteredPosts_list.append({
            "id" : obj.post_id,
            "writer" : obj.writer,
            "content" : obj.content,
            "category" : obj.category
        })
    return JsonResponse({
        'status':200,
        'message':'Success',
        'data': filteredPosts_list
    })
