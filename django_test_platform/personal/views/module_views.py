from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from personal.models.module import Module
from personal.models.project import Project
from django.http import HttpResponseRedirect

@login_required
def module_manage(request):
    module_all = Module.objects.all()
    project_all = Project.objects.all()
    return render(request, "module.html", {"modules": module_all, "projects": project_all, "type": "list"})

@login_required
def add_module(request):
    project_all = Project.objects.all()
    if request.method == "GET":
        return render(request, "module.html", {"projects": project_all, "type": "add"})
    elif request.method == "POST" and "Add" in request.POST:
        module_name = request.POST.get("module_name", "")
        module_describe = request.POST.get("module_describe", "")
        module_project_id = request.POST.get("module_project_id", "")
        if module_name == "":
            return render(request, "module.html", {"projects": project_all, "type": "add", "error": "请输入模块名称"})
        else:
            Module.objects.create(name=module_name,describe=module_describe,project_id=module_project_id)
            return HttpResponseRedirect("/module/")
    elif request.method == "POST" and "Cancel" in request.POST:
        return HttpResponseRedirect("/module/")

@login_required
def edit_module(request,mid):
    project_all = Project.objects.all()
    if request.method == "GET":
        if mid:
            module = Module.objects.get(id=mid)
        return render(request, "module.html", {"module": module, "projects": project_all, "type": "edit", "id": mid})
    elif request.method == "POST" and "Edit" in request.POST:
        if mid:
            module = Module.objects.get(id=mid)
        module_name = request.POST.get("edit_module_name", module.name)
        module_project_id = request.POST.get("edit_module_project_id", module.project_id)
        module_describe = request.POST.get("edit_module_describe", module.describe)
        if module_name == "":
            return render(request, "module.html", {"module": module, "type": "edit", "error": "模块名称不可改为空"})
        else:
            module = Module.objects.get(id=mid)
            module.name = module_name
            module.describe = module_describe
            module.project_id = module_project_id
            module.save()
        return HttpResponseRedirect("/module/")
    elif request.method == "POST" and "Cancel" in request.POST:
        return HttpResponseRedirect("/module/")

@login_required
def delete_module(request,mid):
    if request.method == "GET":
        if mid:
            module = Module.objects.get(id=mid)
            module.delete()
        return HttpResponseRedirect("/module/")