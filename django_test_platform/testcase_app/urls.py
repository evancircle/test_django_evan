from testcase_app import views
from django.urls import path

urlpatterns = [
    # 项目管理
    path('', views.testcase_manage),
    path('debug', views.debug),

]