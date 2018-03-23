# -*-coding:utf-8 -*-
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User  # django 自带后台管理模块
from django.contrib import auth
from models import *


# 主页
def index(request):
    username = request.session.get('username', '')
    content = {'active_menu': 'homepage', 'user': username}
    return render(request, 'index.html', content)                  # 将数据返回到前台


# 注册
def regist(request):
    if request.session.get('username', ''):                        # 获取session用来判断用户是否登录
        return HttpResponseRedirect('/')
    status = ""
    if request.POST:
        username = request.POST.get("username", "")             # 从前台获得用户注册信息，判断，存入数据库
        if User.objects.filter(username=username):
            status = "user_exist"
        else:
            password = request.POST.get("password", "")
            repassword = request.POST.get("repassword", "")
            if password != repassword:
                status = "re_err"
            else:
                newuser = User.objects.create_user(username=username, password=password)
                newuser.save()
                new_myuser = MyUser(user=newuser, phone=request.POST.get("phone"))
                new_myuser.save()
                status = "success"
                return HttpResponseRedirect("/login/")
    return render_to_response("regist.html", {"active_menu": "hompage", "status": status, "user": ""}, context_instance=RequestContext(request))


# 登录
def login(request):
    if request.session.get('username', ''):
        return HttpResponseRedirect('/')
    status = ""
    if request.POST:
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = auth.authenticate(username=username, password=password)
        if user is not None:
                auth.login(request, user)
                request.session["username"] = username       # 保存登录会话
                return HttpResponseRedirect('/')
        else:
            status = "not_exist_or_passwd_err"
    return render(request, "login.html", {"status": status}, context_instance=RequestContext(request))


# 退出登录
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


# 获取学院列表
def get_acad_list():
    room_list = ConfeRoom.objects.all()  # 对数据库的操作
    acad_list = set()
    for room in room_list:
        acad_list.add(room.acad)
    return list(acad_list)


# 查看会议室
def viewroom(request):
    username = request.session.get('username', '')
    if username != '':
        user = MyUser.objects.get(user__username=username)
    else:
        user = ''
    acad_list = get_acad_list()
    room_acad = request.GET.get("acad", "all")  # 从前台点击选择学院，
    if room_acad not in acad_list:  # 如果没有就全部显示
        room_acad = "all"
        room_list = ConfeRoom.objects.all()
    else:
        room_list = ConfeRoom.objects.filter(acad=room_acad)  # 只显示选定学院的会议室
    content = {"active_menu": 'viewroom', "acad_list": acad_list, "room_acad": room_acad, "room_list": room_list,
               "user": user}
    return render_to_response('viewroom.html', content, context_instance=RequestContext(request))


# 会议室详情
def detail(request):
    username = request.session.get('username', '')
    if username != '':
        user = MyUser.objects.get(user__username=username)
    else:
        user = ''
    Id = request.GET.get("id", "")  # 获得会议室主键ID号
    request.session["id"] = Id
    if Id == "":
        return HttpResponseRedirect('/viewroom/')
    try:
        room = ConfeRoom.objects.get(pk=Id)  # 根据ID显示详细信息
        ro = Detail.objects.get(pk=Id)
    except:
        return HttpResponseRedirect('/viewroom/')
    img_list = Detail.objects.filter(room=room)
    num_list = get_order_list()
    if room.num not in num_list:  # 判断是否被预定，给定状态，给前台显示是否可以预定
        or_sta = "yes"
    else:
        or_sta = "no"
    content = {"active_menu": "viewroom", "room": room, "img_list": img_list, "ro": ro, "or_sta": or_sta, "user": user}
    return render_to_response('detail.html', content)


# 预定
# 获取预定列表
def get_order_list():
    num_list = set()
    order_list = Order.objects.all()
    for order in order_list:
        num_list.add(order.num)
    return list(num_list)


def order(request):
    username = request.session.get('username', '')
    if username != '':
        user = MyUser.objects.get(user__username=username)
    else:
        user = ''
    roid = request.session.get("id", "")  # 预定，将数据保存到数据库
    room = ConfeRoom.objects.get(pk=roid)
    time = Detail.objects.get(name=room.name)
    u = MyUser.objects.get(user__username=username)
    order = Order(user=username, num=room.num, name=room.name, time=time.time, size=room.size, phone=u.phone)
    order.save()
    return render_to_response("index2.html", {"user": user}, context_instance=RequestContext(request))


# 查看预定信息
def myorder(request):
    username = request.session.get('username', '')
    if username != '':
        user = MyUser.objects.get(user__username=username)
    else:
        user = ''
    try:
        my_order = Order.objects.all()  # 索引数据库查看已预订信息
        us_sta = "no"
        return render_to_response("myorder.html", {"myorder": my_order, "us_sta": us_sta, "user": user},
                                  context_instance=RequestContext(request))

    except:
        us_sta = "yes"
        return render_to_response("myorder.html", {"us_sta": us_sta, "user": user},
                                  context_instance=RequestContext(request))


# 取消预定
def cancel(request):
    username = request.session.get('username', '')
    if username != '':
        user = MyUser.objects.get(user__username=username)
    else:
        user = ''
    Id = request.GET.get("id", "")  # 取消预订，删除数据
    room = Order.objects.get(pk=Id)
    room.delete()
    return render_to_response("index.html", context_instance=RequestContext(request))

