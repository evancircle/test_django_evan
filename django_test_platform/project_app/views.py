from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from project_app.models import Project
from module_app.models import Module

@login_required
def project_manage(request):
    #项目管理列表
    project_all = Project.objects.all()
    return render(request, "project.html", {"projects": project_all, "type": "list"})

@login_required
def add_project(request):
    #添加项目
    if request.method == "GET":
        return render(request, "project.html", {"type": "add"})
    elif request.method == "POST" and "Add" in request.POST:
        project_name = request.POST.get("project_name", "")
        project_status = request.POST.get("project_status", "")
        project_describe = request.POST.get("project_describe", "")
        if project_name == "":
            return render(request, "project.html", {"type": "add", "error": "请输入项目名称"})
        else:
            Project.objects.create(name=project_name,describe=project_describe,status=project_status)
            return HttpResponseRedirect("/project/")
    elif request.method == "POST" and "Cancel" in request.POST:
        return HttpResponseRedirect("/project/")

@login_required
def edit_project(request,pid):
    #编辑项目
    if request.method == "GET":
        if pid:
            project = Project.objects.get(id=pid)
        return render(request, "project.html", {"project": project, "type": "edit", "id": pid})
    elif request.method == "POST" and "Edit" in request.POST:
        if pid:
            project = Project.objects.get(id=pid)
        project_name = request.POST.get("edit_project_name", project.name)
        project_status = request.POST.get("edit_project_status", project.status)
        project_describe = request.POST.get("edit_project_describe", project.describe)
        if project_name == "":
            return render(request, "project.html", {"project": project, "type": "edit", "error": "项目名称不可改为空"})
        else:
            project = Project.objects.get(id=pid)
            project.name = project_name
            project.describe = project_describe
            project.status = project_status
            project.save()
        return HttpResponseRedirect("/project/")
    elif request.method == "POST" and "Cancel" in request.POST:
        return HttpResponseRedirect("/project/")

@login_required
def delete_project(request,pid):
    #删除列表
    if request.method == "GET":
        if pid:
            try:
                project = Project.objects.get(id=pid)
            except Project.DoesNotExist:
                return HttpResponseRedirect("/project/")
            if Module.objects.filter(project_id=project.id).exists():
                for module in Module.objects.filter(project_id=project.id):
                    module.delete()
                project.delete()
            else:
                project.delete()
        return HttpResponseRedirect("/project/")
    else:
        return HttpResponseRedirect("/project/")