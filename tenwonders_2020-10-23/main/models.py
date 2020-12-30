from django.db import models
from login.models import Account
from django.utils import timezone


# Create your models here.

class Search(models.Model):
    search = models.CharField(max_length = 20)
    def __str__(self):
        return self.search

class Youtube_result(models.Model):
    channel_name = models.CharField(max_length = 100)
    subscriber_num =  models.FloatField() 
    not_int_subscriber_num = models.CharField(max_length = 100)
    profile_url = models.CharField(max_length = 100)
    def __str__(self):
        return self.channel_name

class Instagram_result(models.Model):
    insta_id = models.CharField(max_length=50)
    profile_url = models.CharField(max_length=100)
    def __str__(self):
        return self.insta_id

class Work(models.Model):
    name = models.CharField(max_length=30,verbose_name="업무 이름")
    content = models.TextField(verbose_name="업무 내용")
    assigned_worker = models.ManyToManyField(Account, verbose_name=("배정된 직원"))
    file = models.FileField(upload_to='files/')
    def __str__(self):
        return self.name



class Log(models.Model):
    work = models.ForeignKey(Work,on_delete=models.CASCADE)
    worker = models.ForeignKey(Account,on_delete=models.CASCADE) 
    date = models.DateTimeField(default=timezone.now(), null=True)
    def __str__(self):
        return self.date

class ID_btn(models.Model):
    celly_id = models.CharField(max_length=20,default="default_id")
    celly_pw = models.CharField(max_length=20,default='default_pw')
    now_using = models.BooleanField(default=False)
    using_worker = models.CharField(max_length=20, default="null")
    dm_blocked = models.BooleanField(default=False)
    def __str__(self):
        return self.celly_id

class Influencer_DB(models.Model):
    name = models.CharField(max_length = 20)
    gender = models.CharField(max_length = 5)
    phone_num = models.CharField(max_length = 20)
    email = models.CharField(max_length = 30)
    address = models.CharField(max_length = 80)
    insta_url = models.CharField(max_length = 80)
    follower = models.CharField(max_length = 30)
    brand_name = models.CharField(max_length = 20)
    keyword = models.CharField(max_length = 80)
    product = models.CharField(max_length = 100)
    def __str__(self):
        return self.name

class Notice(models.Model):
    status = models.CharField(max_length = 20)
    title = models.CharField(max_length = 20)
    content = models.TextField()
    writer = models.ForeignKey(Account,on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now(), null=True)
    visit_num = models.IntegerField(default=0)
    def __str__(self):
        return self.title

class Meeting(models.Model):
    name = models.ForeignKey(Account,on_delete=models.CASCADE)
    company = models.CharField(max_length=50,verbose_name="회사명")
    date = models.DateTimeField(default=timezone.now(), null=True) 
    encharge_name = models.CharField(max_length=20,verbose_name="담당자명")
    position = models.CharField(max_length=20, verbose_name="직책")
    phone_num = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    company_address = models.TextField(verbose_name="회사 주소")
    etc = models.TextField(verbose_name="특이사항")
    def __str__(self):
        return self.company

class Schedule(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    day = models.CharField(max_length=10,verbose_name="요일")
    
