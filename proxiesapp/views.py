from django.http import HttpResponse
from django.shortcuts import render
from proxiesapp.writeProxy.storageModule import RedisClient
# Create your views here.
"""配置路由"""
def get_conn():
    return RedisClient.RedisClient()
#随机获取代理
def random(request):
    conn = get_conn()
    random_result = conn.get_random_proxy()
    #return HttpResponse(random_result)   #页面返回简单的字符串
    return render(request,"../templates/web.html",context={"random_result":random_result})   #返回H5页面
#获取代理总数
def count(request):
    conn = get_conn()
    count = conn.hcount()
    #return HttpResponse(count)   #页面返回简单的字符串
    return render(request,"../templates/web.html",context={"count":count})   #返回H5页面
#列表形式返回全部代理
def all_proxy(request):
    conn = get_conn()
    all_proxy = conn.hgetAll()#返回的是列表
    return render(request,"../templates/web.html",context={"all_proxy":all_proxy})
