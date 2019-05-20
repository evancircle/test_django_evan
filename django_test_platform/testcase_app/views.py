from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import requests
import json
from testcase_app.models import TestCase
from module_app.models import Module

# Create your views here.
@login_required
def testcase_manage(request):
    #用例列表
    case_list = TestCase.objects.all()
    return render(request, "case_list.html", {"cases": case_list})

@login_required
def add_case(request):
    #添加用例
    return render(request, "case_add.html")

@login_required
def edit_case(request, cid):
    #编辑用例
    return render(request, "case_edit.html")

@login_required
def testcase_debug(request):
    #测试用例的调试
    global req, payload
    if request.method == "POST":
        url = request.POST.get("url", "")
        request_mothed = request.POST.get("method", "")
        header = request.POST.get("header", "")
        request_type = request.POST.get("parameter_type", "")
        parameter = request.POST.get("parameter", "")

        if header != '':
            json_header = header.replace("\'", "\"")
            try:
                header = json.loads(json_header)
            except json.decoder.JSONDecodeError:
                return JsonResponse({"result": "header类型错误"})
        else:
            pass

        if parameter != '':
            json_par = parameter.replace("\'", "\"")
            try:
                payload = json.loads(json_par)
            except json.decoder.JSONDecodeError:
                return JsonResponse({"result": "参数类型错误"})
        else:
            pass

        if request_mothed == "get":
            if header == "" and parameter == '':
                req = requests.get(url)
            elif header == "":
                req = requests.get(url, params=payload)
            else:
                req = requests.get(url, params=payload, headers=header)

        if request_mothed == "post":
            if request_type == "form":
                if header == "" and parameter == '':
                    req = requests.post(url)
                elif header == "":
                    req = requests.post(url, data=payload)
                else:
                    req = requests.post(url, data=payload, headers=header)

            if request_type == "json":
                if header == "" and parameter == '':
                    req = requests.post(url)
                elif header == "":
                    req = requests.post(url, json=payload)
                else:
                    req = requests.post(url, json=payload, headers=header)

        if request_mothed == "put":
            if header == "" and parameter == '':
                req = requests.put(url)
            elif header == "":
                req = requests.put(url, params=payload)
            else:
                req = requests.put(url, params=payload, headers=header)

        if request_mothed == "delete":
            if header == "" and parameter == '':
                req = requests.delete(url)
            elif header == "":
                req = requests.delete(url, params=payload)
            else:
                req = requests.delete(url, params=payload, headers=header)

        return JsonResponse({"result": req.text})
    else:
        return JsonResponse({"result": "请求方法错误"})

@login_required
def testcase_assert(request):
    #测试用例的断言
    if request.method == "POST":
        result_text = request.POST.get("result", "")
        assert_text = request.POST.get("assert", "")
        assert_type = request.POST.get("assert_type", "")

        if result_text == "" or assert_text == "":
            return JsonResponse({"result": "断言的文本不能为空"})

        if assert_type == "contains":
            assert_list = assert_text.split(">>")
            for assert_value in assert_list:
                if assert_value not in result_text:
                    return JsonResponse({"result": "断言失败"})
                else:
                    return JsonResponse({"result": "断言成功"})

        elif assert_type == "mathches":
            if assert_text != result_text:
                return JsonResponse({"result": "断言失败"})
            else:
                return JsonResponse({"result": "断言成功"})

    else:
        return JsonResponse({"result": "请求方法错误"})

@login_required
def testcase_save(request):
    #用例保存
    if request.method == "POST":
        url = request.POST.get("url", "")
        method = request.POST.get("method", "")
        header = request.POST.get("header", "")
        parameter_type = request.POST.get("par_type", "")
        parameter_body = request.POST.get("par_body", "")
        assert_type = request.POST.get("ass_type", "")
        assert_text = request.POST.get("ass_text", "")
        module_id = request.POST.get("mid", "")
        name = request.POST.get("name", "")

        print("url", url)
        print("method", method)
        print("header", header)
        print("parameter_type", parameter_type)
        print("parameter_body", parameter_body)
        print("assert_type", assert_type)
        print("assert_text", assert_text)
        print("module_id", module_id)
        print("name", name)

        if name == "":
            return JsonResponse({"status": 10101, "message": "用例名称不能为空"})

        if module_id == "":
            return JsonResponse({"status": 10103, "message": "所属的模块不能为空"})

        if assert_type == "" or assert_text == "":
            return JsonResponse({"status": 10102, "message": "断言的类型或文本不能为空"})

        # ...
        if method == "get":
            module_number = 1
        elif method == "post":
            module_number = 2
        elif method == "delete":
            module_number = 3
        elif method == "put":
            module_number = 4
        else:
            return JsonResponse({"status": 10104, "message": "未知的请求方法"})

        if parameter_type == "form":
            parameter_number = 1
        elif parameter_type == "json":
            parameter_number = 2
        else:
            return JsonResponse({"status": 10104, "message": "未知的参数类型"})

        if assert_type == "contains":
            assert_number = 1
        elif assert_type == "mathches":
            assert_number = 2
        else:
            return JsonResponse({"status": 10104, "message": "未知的断言类型"})

        ret = TestCase.objects.create(name=name, module_id=module_id,
                                      url=url, method=module_number, header=header,
                                      parameter_type=parameter_number, parameter_body=parameter_body,
                                      assert_type=assert_number, assert_text=assert_text)
        print(ret)

        return JsonResponse({"status": 10200, "message": "创建成功！"})

    else:
        return JsonResponse({"status": 10100, "message": "请求方法错误"})

def get_case_info(request):
    #获取用例数据接口
    if request.method == "POST":
        cid = request.POST.get("cid", "")
        case = TestCase.objects.get(id=cid)
        module = Module.objects.get(id=case.module.id)
        project_id = module.project.id;

        case_dict = {
            "id": case.id,
            "url": case.url,
            "name": case.name,
            "method": case.method,
            "header": case.header,
            "parameter_type": case.parameter_type,
            "parameter_body": case.parameter_body,
            "assert_type": case.assert_type,
            "assert_text": case.assert_text,
            "module_id": case.module.id,
            "project_id": project_id,
        }
        return JsonResponse({"status": 10200,"message": "请求成功","data": case_dict})

    else:
        return JsonResponse({"status": 10100, "message": "请求方法错误"})