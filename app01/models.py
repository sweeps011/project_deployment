from django.db import models

"""部门表"""
class Department(models.Model):
    title = models.CharField(verbose_name="部门名",max_length=32)

    def __str__(self):
        return self.title

"""员工表"""
class Userinfo(models.Model):
    name = models.CharField(verbose_name="姓名",max_length=16)
    password = models.CharField(verbose_name="密码",max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="工资",max_digits=10,decimal_places=2,default=0)
    createtime = models.DateField(verbose_name="入职时间")
    #不加约束
    #depart_id = models.BigIntegerField(verbose_name="部门号")

    #加约束,级联删除，使用foreignky depart后面自动加_id
    depart = models.ForeignKey(verbose_name="部门",to = "Department",to_field="id",null=True,blank=True,on_delete=models.SET_NULL)

   #在django中约束
    gender_choices ={
        (1,"男"),
        (2,"女")
    }
    gender = models.SmallIntegerField(verbose_name="性别",choices=gender_choices)


"""管理员"""
class Admin(models.Model):
    username = models.CharField(verbose_name="用户名",max_length=32)
    password = models.CharField(verbose_name="密码",max_length=32)