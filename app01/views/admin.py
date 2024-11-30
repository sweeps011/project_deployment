from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from app01 import models
from app01.utils.form import Adminmodelform, Admin_change_modelform, Admin_change_password_modelform
from django.core.exceptions import ValidationError

def admin_list(request):

    info = request.session.get("info")

    if not info:
        return redirect("/login/")

    list_dict = {}
    value = request.GET.get('search')

    if value:
        list_dict["username__contains"] = value
    queryset = models.Admin.objects.filter(**list_dict).order_by('id')
    posts_per_page = 10
    paginator = Paginator(queryset, posts_per_page)
    page_number = request.GET.get('page', 1)
    try:
        # 获取指定页码的页面数据
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # 如果页码不存在，返回第一页数据作为默认
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'admin_list.html', {"page_obj": page_obj})


def admin_add(request):
    if request.method == "GET":
        form = Adminmodelform
        return render(request, "admin_add.html", {'form': form})
    form = Adminmodelform(data=request.POST)
    if form.is_valid():
        password = form.cleaned_data.get('password')
        again_password = form.cleaned_data.get('again_password')
        try:
            new_admin = form.save(commit=False)  # 先不提交到数据库
            existing_admin = models.Admin.objects.filter(username=new_admin.username).first()
            if existing_admin:
                form.add_error('username', '该用户名已存在，请更换用户名')  # 给username字段添加错误提示
                return render(request, "admin_add.html", {'form': form})
            if password != again_password:
                form.add_error('again_password', '确认密码与密码不一致，请重新输入')
                return render(request, "admin_add.html", {'form': form})
            new_admin.save()  # 保存到数据库
            return redirect("/admin/list")
        except ValidationError as e:
            form.add_error(None, str(e))  # 处理其他可能的验证错误并添加到表单错误里
            return render(request, "admin_add.html", {'form': form})
    return render(request, "admin_add.html", {'form': form})



def admin_delete(request):
    nid = request.GET.get('nid')
    models.Admin.objects.filter(id=nid).delete()
    return redirect("/admin/list")


def admin_change(request,id):
    row_object = models.Admin.objects.filter(id=id).first()

    if request.method == "GET":

        form = Admin_change_modelform(instance=row_object)
        return render(request, "admin_change.html", {'form':form})

    form = Admin_change_modelform(data=request.POST,instance=row_object)
    """前面获取的row_object,到了form.is_valid()会改变"""
    if form.is_valid():
        # password = form.cleaned_data.get('password')
        # again_password = form.cleaned_data.get('again_password')

        try:
            new_admin = form.save(commit=False)  # 先不提交到数据库

            row_object = models.Admin.objects.filter(id=id).first()
            print(new_admin.username)
            print(row_object.username)

            if (new_admin.username == row_object.username):
                # and (models.Admin.objects.filter(username=new_admin.username).exclude(id=id).exists())
                form.add_error('username', '无需修改')  # 给username字段添加错误提示
                return render(request, "admin_add.html", {'form': form})
            elif (new_admin.username!= row_object.username)and (models.Admin.objects.filter(username=new_admin.username).exclude(id=id).exists()):

                form.add_error('username', '该用户名已存在，请更换用户名')  # 给username字段添加错误提示
                return render(request, "admin_add.html", {'form': form})
            # if password != again_password:
            #     form.add_error('again_password', '确认密码与密码不一致，请重新输入')
            #     return render(request, "admin_add.html", {'form': form})
            new_admin.save()  # 保存到数据库
            return redirect("/admin/list")
        except ValidationError as e:
            form.add_error(None, str(e))  # 处理其他可能的验证错误并添加到表单错误里
            return render(request, "admin_add.html", {'form': form})
        form.save()
        return redirect('/admin/list')
    return render(request, "admin_list.html", {'form': form})

def admin_change_password(request,id):
    row_object = models.Admin.objects.filter(id=id).first()

    if request.method == "GET":
        form = Admin_change_password_modelform(instance=row_object)
        return render(request, "admin_change.html", {'form': form})

    form = Admin_change_password_modelform(data=request.POST, instance=row_object)
    """前面获取的row_object,到了form.is_valid()会改变"""
    if form.is_valid():
        password = form.cleaned_data.get('password')
        again_password = form.cleaned_data.get('again_password')

        try:
            new_admin = form.save(commit=False)  # 先不提交到数据库

            row_object = models.Admin.objects.filter(id=id).first()
            print(new_admin.password)
            print(row_object.password)
            print(password)
            print(again_password)

            if (new_admin.password == row_object.password):
                # and (models.Admin.objects.filter(username=new_admin.username).exclude(id=id).exists())
                form.add_error('password', '无需修改')  # 给username字段添加错误提示
                return render(request, "admin_change_password.html", {'form': form})
            elif (password != again_password):

                form.add_error('again_password', '密码不一致')  # 给username字段添加错误提示
                return render(request, "admin_change_password.html", {'form': form})
            # if password != again_password:
            #     form.add_error('again_password', '确认密码与密码不一致，请重新输入')
            #     return render(request, "admin_add.html", {'form': form})
            new_admin.save()  # 保存到数据库
            return redirect("/admin/list")
        except ValidationError as e:
            form.add_error(None, str(e))  # 处理其他可能的验证错误并添加到表单错误里
            return render(request, "admin_change_password.html", {'form': form})
        form.save()
        return redirect('/admin/list')
    return render(request, "admin_list.html", {'form': form})

