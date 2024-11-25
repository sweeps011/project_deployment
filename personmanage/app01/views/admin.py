from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from app01 import models
from app01.utils.form import Adminmodelform
from django.core.exceptions import ValidationError

def admin_list(request):
    list_dict = {}
    value = request.GET.get('search')

    if value:
        list_dict["username__contains"] = value
    queryset = models.Admin.objects.filter(**list_dict)
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
        try:
            new_admin = form.save(commit=False)  # 先不提交到数据库
            existing_admin = models.Admin.objects.filter(username=new_admin.username).first()
            if existing_admin:
                form.add_error('username', '该用户名已存在，请更换用户名')  # 给username字段添加错误提示
                return render(request, "admin_add.html", {'form': form})
            new_admin.save()  # 保存到数据库
            return redirect("/admin/list")
        except ValidationError as e:
            form.add_error(None, str(e))  # 处理其他可能的验证错误并添加到表单错误里
            return render(request, "admin_add.html", {'form': form})
    return render(request, "admin_add.html", {'form': form})
