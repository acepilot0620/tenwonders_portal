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

class Contract(models.Model):
    name = models.CharField(max_length=30)
    category = models.CharField(max_length=30)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    def __str__(self):
        return self.name

class Record(models.Model):
    contract = models.ForeignKey(Contract,on_delete=models.CASCADE)
    insta_id = models.CharField(max_length=30)
    writer = models.CharField(max_length=10,default="default_id")
    influencer = models.CharField(max_length=30)
    #바꾸기 귀찮아서 안바꿈 feed_condition아니라  DM내용임
    feed_condition = models.TextField(max_length=1000)
    is_confirmed = models.BooleanField()
    def __str__(self):
        return self.influencer

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
    