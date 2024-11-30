from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from app01 import models
from app01.utils.form import Adminmodelform, Admin_change_modelform, Admin_change_password_modelform, login_modelform
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login
def account_login(request):
    # if request.method == 'POST':
    #     form = login_modelform(request.POST)
    #
    #     if form.is_valid():
    #         username = form.cleaned_data['username']
    #         password = form.cleaned_data['password']
    #         print(username)
    #         print(password)
    #         user = authenticate(request, username=username, password=password)
    #         print(user)
    #         if user is not None:
    #             login(request, user)
    #             return redirect('/depart/list')  # 登录成功后重定向到主页，根据实际情况修改
    #         else:
    #             form.add_error(None, '用户名或密码错误')
    #             return render(request, "login.html", {'form': form})
    # else:
    #     form = login_modelform()
    # return render(request, 'login.html', {'form': form})


    if request.method == "GET":
        form = login_modelform()
        return render(request, "login.html", {'form': form})

    form = login_modelform(data=request.POST)

    """前面获取的row_object,到了form.is_valid()会改变"""
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        print(username)
        print(password)

        row_object = models.Admin.objects.filter(username=username,password=password).first()
        print(row_object)

        if  row_object  is not None:
            request.session["info"] = {"id":row_object.id,"name":row_object.username}
            return redirect('/depart/list')
        else:
            form.add_error('password', '用户名或密码错误')
            return render(request, "login.html", {'form': form})


def account_out(request):
    request.session.clear()
    return render(request,'login.html')



