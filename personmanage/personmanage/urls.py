"""
URL configuration for personmanage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01 import views
from app01.views import user,depart,admin
urlpatterns = [
    #    path('admin/', admin.site.urls),
    #      部门管理
         path('depart/list',depart.depart_list),
         path('depart/add',depart.depart_add),

         path('depart/modelform/add',depart.depart_add_modelform),

         path('depart/delete',depart.depart_delete),
         path('depart/<int:nid>/change',depart.depart_change),



        # 用户管理
         path('user/list',user.user_list),
         path('user/add',user.user_add),
         path('user/modelform/add',user.user_modelformadd),
         path('user/delete',user.user_delete),
         path('user/<int:id>/change',user.user_change),

        #管理员
         path('admin/list',admin.admin_list),
         path('admin/add',admin.admin_add)

]
