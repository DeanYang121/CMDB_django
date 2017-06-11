from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from CMDB.models import User
#from importlib import import_module
#from django.conf import settings
from functools import wraps
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
import hashlib
import os

# Create your views here.
# SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
# session = SessionStore()

def login_requried(func):
    @wraps(func)
    def wrapper(request,*args,**kwargs):
        if request.session.get('username',None) is None:
            return HttpResponseRedirect("/")
        rt = func(request,*args,**kwargs)
        return rt
    return wrapper

@csrf_exempt
def index(request):
    return render(request,'login.html')

@login_requried
def index1(request):
    username = request.session.get("username")
    context = {"username":username}
    return render(request, 'index1.html',context)

def login(request):
    if request.method == "POST":
        usr = request.POST["username"]
        pwd = request.POST["password"]
        try:
            has_username = User.objects.get(username=usr)
        except ObjectDoesNotExist as e:
            has_username = False
        if has_username:
            password = hashlib.sha1(pwd.encode("utf8")+usr.encode("utf8")).hexdigest()
            name = User.objects.get(username=usr).username
            is_login = User.objects.filter(username=usr,password=password)
            if is_login:
                context = {"username":name}
                # session["username"]= name  session.save()
                request.session["username"]=name #添加session
                return render(request, 'index1.html',context)
            else:
                context = {"error":"密码错误","username":usr}
                return render(request, 'login.html', context)
        else:
            context = {"error":"用户名不存在"}
            return render(request, 'login.html',context)
    else:
        context = {"error":"请求不合法"}
        return render(request, 'login.html',context)



@login_requried
def users(request):
    username = request.session.get("username")
    context = {"username":username,}
    return render(request,"users.html",context)

@login_requried
def nginx(request):
    file = open("nginx.conf","r+")
    content = file.read()
    file.close()
    #print(content)
    username = request.session.get("username")
    context = {"username":username,"content":content}
    return render(request,"nginx.html",context)

@csrf_exempt
@login_requried
def modify_nginx(request):
    username = request.session.get("username")
    context = {"username":username,}
    if request.method == "POST":
        data = request.POST["nginx"]
        #print(data)
        modify = open('update.conf','w')
        modify.write(data)
        modify.close()
    try:
        os.remove('nginx.conf')
        g = open('update.conf', 'r')
        f = open('nginx.conf', 'w+')
        for line in g.readlines():
            if len(line.strip()) == 0:
                continue
            else:
                f.write(line)
    finally:
        g.close()
        f.close()
    username = request.session.get("username")
    context = {"username":username}
    return HttpResponseRedirect("/nginx/")

@login_requried
def assets(request):
    return render(request,"assets.html")

@login_requried
def web_ssh(request):
    return render(request,'gateone.html')

@login_requried
def logout(request):
    del request.session["username"]
    return HttpResponseRedirect("/")

@login_requried
def detail(request,id):
    return HttpResponse("detail %s" % id)
