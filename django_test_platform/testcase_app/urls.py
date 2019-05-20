from testcase_app import views
from django.urls import path

urlpatterns = [
    # 项目管理
    path('', views.testcase_manage),
    path('add_case/', views.add_case),
    path('edit_case/<int:cid>/', views.edit_case),

    path('get_case_info', views.get_case_info),
    path('debug', views.testcase_debug),
    path('assert', views.testcase_assert),
    path('save_case', views.testcase_save),
]