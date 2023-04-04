from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import Post

# Create your views here.

def hello_world(request):
    if request.method == "GET":
        return JsonResponse({
            "status" : 200,
            "success" : True,
            "message" : "Message delivered!",
            "data" : "Hello World!",
        })
    
@require_http_methods(["GET"])
def get_post_detail(resquest, id):
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

def get_all_posts(resquest):
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