from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
import json

# Create your views here.
def testcase_manage(request):
    return render(request, "testcase.html", {"type": "debug"})


def debug(request):
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
            if request_type == "form-data":
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