from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
    # 장고 유저와 내가 만든 모델 1대1 연결
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.TextField(max_length="20")
    position = models.TextField(max_length="20")
    
    def __str__(self):
        return self.nickname
    
    class Meta:
        ordering=['id'] # 오름차순 정렬
        #ordering=['-id] 내림차순

    # 다른곳에서도 필요하다면 model에서 구현하면 되고 Admin에서만 필요하면 어드민에서 구현해도 상관 없음   
    # def nickname_length(self):
    #     return len(self.nickname)
    # nickname_length.short_description = "닉네임 글자수"

    