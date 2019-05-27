from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from module_app.models import Module
from project_app.models import Project
from testcase_app.models import TestCase
from django.http import HttpResponseRedirect, JsonResponse

@login_required
def module_manage(request):
    #模块管理列表
    module_all = Module.objects.all()
    project_all = Project.objects.all()
    return render(request, "module.html", {"modules": module_all, "projects": project_all, "type": "list"})

@login_required
def add_module(request):
    #添加模块
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
def edit_module(request, mid):
    #编辑模块
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
def delete_module(request, mid):
    #删除模块
    if request.method == "GET":
        if mid:
            try:
                module = Module.objects.get(id=mid)
            except Project.DoesNotExist:
                return HttpResponseRedirect("/module/")
            if TestCase.objects.filter(module_id=module.id).exists():
                for case in TestCase.objects.filter(module_id=module.id):
                    case.delete()
                module.delete()
            else:
                module.delete()
        return HttpResponseRedirect("/module/")
    else:
        return HttpResponseRedirect("/module/")

# @login_required
# def get_module_list(request):
#     #接口：根据项目id,获取对应的模块列表
#     if request.method == "POST":
#         pid = request.POST.get("pid", "")
#         if pid == "":
#             return JsonResponse({"status": 10102,"message": "项目id不能空"})
#
#         modules = Module.objects.filter(project=pid)
#         module_list = []
#         for module in modules:
#             module_dict = {
#                 "id": module.id,
#                 "name": module.name
#             }
#             module_list.append(module_dict)
#         return JsonResponse({"status": 10200, "message": "请求成功","data": module_list})
#     else:
#         return JsonResponse({"status": 10101, "message": "请求方法错误"})
