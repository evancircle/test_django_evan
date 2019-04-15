from module_app import views
from django.urls import path

urlpatterns = [
    #模块管理
    path('', views.module_manage),
    path('add_module/', views.add_module),
    path('edit_module/<int:mid>/', views.edit_module),
    path('delete_module/<int:pid>/', views.delete_module),

]