
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from app01 import models
from django.core.exceptions import ValidationError
import datetime
from app01.utils.form import Usersmodelform,Departmodelform
# Create your views here.



"""用户列表"""
def user_list(request):
    list_dict = {}
    value = request.GET.get('search')
    if value:
        list_dict["name__contains"] = value
    departlist = models.Department.objects.all()
    userlist = models.Userinfo.objects.filter(**list_dict).order_by('id')
    posts_per_page = 10
    paginator = Paginator(userlist, posts_per_page)
    page_number = request.GET.get('page', 1)
    try:
        # 获取指定页码的页面数据
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # 如果页码不存在，返回第一页数据作为默认
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request,"user_list.html",{'userlist':userlist,'departlist':departlist,'page_obj':page_obj})

"""添加用户"""


def user_add(request):
    if request.method == "GET":
        context = {
            'depart_list': models.Department.objects.all()

        }
        return render(request, "user_add.html", context)
    else:
        name = request.POST.get('user')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        depart = request.POST.get('depart')
        createtime = request.POST.get('createtime')
        password = request.POST.get('password')
        createtime = datetime.datetime.strptime(createtime, '%Y/%m/%d').strftime('%Y-%m-%d')

        models.Userinfo.objects.create(name=name, password=password, age=age, createtime=createtime, gender=gender,depart_id=depart)
        return redirect("/user/list")




def user_modelformadd(request):
    if request.method=="GET":
        form = Usersmodelform
        return render(request,"user_modelformadd.html",{'form':form})
    form = Usersmodelform(data=request.POST)
    if form.is_valid():
        try:
            new_user = form.save(commit=False)  # 先不提交到数据库
            existing_user = models.Userinfo.objects.filter(name=new_user.name).first()
            if existing_user:
                form.add_error('name', '该用户已存在')  # 给username字段添加错误提示
                return render(request, "user_modelformadd.html", {'form': form})
            new_user.save()  # 保存到数据库
            return redirect("/user/list")
        except ValidationError as e:
            form.add_error(None, str(e))  # 处理其他可能的验证错误并添加到表单错误里
            return render(request, "user_modelformadd.html", {'form': form})
    return render(request, "user_modelformadd.html", {'form': form})



def user_delete(request):
    nid = request.GET.get('nid')
    models.Userinfo.objects.filter(id=nid).delete()
    return redirect("/user/list")



def user_change(request,id):
    row_object = models.Userinfo.objects.filter(id=id).first()
    if request.method == "GET":

        form = Usersmodelform(instance=row_object)
        return render(request, "user_change.html", {'form':form})

    form = Usersmodelform(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/user/list')
    return render(request, "user_modelformadd.html", {'form': form})

