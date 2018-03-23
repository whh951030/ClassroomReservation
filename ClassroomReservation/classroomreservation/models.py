# !/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User     # 这里调用django的用户管理模块


# 注册用户模型
class MyUser(models.Model):  
    user = models.OneToOneField(User)  # 这里的user与User是一对一的关系
    phone = models.CharField(max_length=11)  # 字符型，必须有个参数max_length字符最大值

    def __unicode__(self):
        return self.user.username   # 返回的对象为username


# 会议室模型
class ConfeRoom(models.Model):  
    num = models.CharField(max_length=5)  
    name = models.CharField(max_length=50)
    size = models.CharField(max_length=5)
    acad = models.CharField(max_length=30)

    class MEAT:                              # 引入MEAT中间件，为了在前端显示的时候以“num”顺序排列，与下一个类似
        ordering = ["num"]  

    def __unicode__(self):
        return self.num  


# 会议室详情
class Detail(models.Model):  
    name = models.CharField(max_length=50)  
    img = models.ImageField(upload_to="image")    #图片类型，参数表示上传图片
    time = models.CharField(max_length=20)
    room = models.ForeignKey(ConfeRoom)    # 这里采用多对一的关系，一个学院有很多会议室，而一个会议室只能属于一个学院

    class MEAT:
        ordering = ["name"]

    def __unicode__(self):  
        return self.name


# 订单信息
class Order(models.Model):  
    user = models.CharField(max_length=30)  
    num = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    time = models.CharField(max_length=20)
    size = models.CharField(max_length=5)
    phone = models.CharField(max_length=11)  
    ntime = models.CharField(max_length=30)

    def __unicode__(self):
        return self.user  
