
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from app01 import models
from app01.utils.form import Usersmodelform,Departmodelform
from django.core.exceptions import ValidationError

"""部门列表"""
def depart_list(request):
    list_dict={}
    value = request.GET.get('search')


    if value:
        list_dict["title__contains"] = value
    queryset = models.Department.objects.filter(**list_dict)
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
    return render(request,'depart_list.html',{"page_obj":page_obj})
"""添加部门"""
def depart_add(request):
    if request.method == "GET":
        return render(request,"depart_add.html")
    else:
        name = request.POST.get("title")
        models.Department.objects.create(title=name)
        return redirect("/depart/list")



def depart_delete(request):
    nid = request.GET.get('nid')
    models.Department.objects.filter(id=nid).delete()
    return redirect("/depart/list")

"""编辑部门"""
def depart_change(request,nid):
    if request.method =="GET":

        row_object = models.Department.objects.filter(id=nid).first()
        return render(request,"depart_change.html",{'row_object':row_object})

    title = request.POST.get('title')
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect("/depart/list")


def depart_add_modelform(request):
    if request.method =="GET":
        form = Departmodelform()
        return render(request,'depart_add_modelform.html',{'form':form})
    form = Departmodelform(data=request.POST)
    if form.is_valid():
        try:
            new_title = form.save(commit=False)  # 先不提交到数据库
            existing_title = models.Department.objects.filter(title=new_title.title).first()
            if existing_title:
                form.add_error('title', '该部门已存在，请更换部门')  # 给username字段添加错误提示
                return render(request, "depart_add_modelform.html", {'form': form})
            new_title.save()  # 保存到数据库
            return redirect("/depart/list")
        except ValidationError as e:
            form.add_error(None, str(e))  # 处理其他可能的验证错误并添加到表单错误里
            return render(request, "depart_add_modelform.html", {'form': form})
    return render(request, "depart_add_modelform.html", {'form': form})






