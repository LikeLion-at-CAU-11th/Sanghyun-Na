from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# Create your views here.
    
def sendIntroduction(request):
    if request.method == "GET":
        return JsonResponse({
            'status' : 200,
            'success' : True,
            'message' : 'Message delivered!',
            'data' : [
                {
                    "name" : "나상현",
                    "GithubID" : "sanghyunna",
                    "major" : "Computer Science and Engineering"
                },
                {
                    "name" : "최은수",
                    "GithubID" : "eunsu02",
                    "major" : "Sociology"
                }
            ]
        })