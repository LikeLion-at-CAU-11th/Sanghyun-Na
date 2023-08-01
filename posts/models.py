from django.db import models
from accounts.models import Member
from storages.backends.s3boto3 import S3Boto3Storage

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name="작성일시", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="수정일시", auto_now=True)

    # 필터를 이용해서 created_at을 활용해서, 오늘 세션 이후, 다음 세션 이전에 만들어진 post들만 모아서 보내주는 api

    class Meta:
        abstract = True

class Post(BaseModel):

    CHOICES = (
        ('DIARY', '일기'),
        ('STUDY', '공부'),
        ('ETC', '기타')
    )

    id = models.AutoField(primary_key=True)
    # writer = models.CharField(verbose_name="작성자", max_length=20)
    writer = models.ForeignKey(to=Member, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="내용")
    category = models.CharField(choices=CHOICES, max_length=20)
    # blank와 null 파라미터를 넣어주어 필수사항에서 제외함
    thumbnail = models.ImageField(verbose_name="썸네일", upload_to="post/thumbnail", blank=True, null=True, storage=S3Boto3Storage())
 

class Comment(BaseModel):
    id = models.AutoField(primary_key=True)
    writer = models.CharField(verbose_name="작성자", max_length=20)
    content = models.CharField(verbose_name="내용", max_length=200)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, blank=False)