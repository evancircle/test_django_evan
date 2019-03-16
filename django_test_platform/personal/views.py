from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    if request.method == "GET":
        return render(request,"index.html")
    else:
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        if username == "" or password == "":
            return render(request, "index.html", {"error": "请输入你的用户名/密码"})

        user = auth.authenticate(username=username,password=password)

        if user is None:
            return render(request, "index.html", {"error": "用户名/密码错误"})

        else:
            auth.login(request,user)
            return HttpResponseRedirect("/project/")

@login_required
def project_manage(request):
    return render(request, "project.html")

@login_required
def module_manage(request):
    return render(request, "module.html")

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/index/")
