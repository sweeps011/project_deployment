
from django import forms
from app01 import models
from app01.utils.bootstrapmodelform import bootstarp


class Usersmodelform(bootstarp):
    name = forms.CharField(min_length=3,label="姓名")
    class Meta:
        model = models.Userinfo
        fields = ["name","age","gender","depart","createtime","password"]
    def __str__(self):
        return self.title


class Departmodelform(bootstarp):
        class Meta:
            model = models.Department
            fields = ['title']

class Adminmodelform(bootstarp):
        again_password = forms.CharField(label="确认密码")
        class Meta:
            model = models.Admin
            fields = ["username","password","again_password"]


class Admin_change_modelform(bootstarp):
        class Meta:
            model = models.Admin
            fields = ["username"]


class Admin_change_password_modelform(bootstarp):
    again_password = forms.CharField(label='确认密码')
    class Meta:
        model = models.Admin
        fields = ["password","again_password"]


class login_modelform(bootstarp):
    class Meta:
        model = models.Admin
        fields = ['username','password']
        widgets = {
            'password': forms.PasswordInput()
        }