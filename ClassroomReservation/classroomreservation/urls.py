from django.conf.urls import url
from classroomreservation import views
urlpatterns =[
    url(r'^$', views.index, name='index'),
    url(r'^regist/$', views.regist, name='regist'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^cancel/$', views.cancel, name='cancal'),
    url(r'^myorder/$', views.myorder, name='myorder'),
    url(r'^viewroom/$', views.viewroom, name='viewroom'),
    url(r'^detail/$', views.detail, name='detail'),
    url(r'^order/$', views.order, name='order'),
]