#-*- coding:utf-8 -*-

from django import forms
from django.forms import ModelForm
from manager.models import Blog,Category
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from ckeditor.widgets import CKEditorWidget
from ckeditor.fields import RichTextFormField
from wmd.widgets import MarkDownInput
# class loginForm(forms.Form):
#     un=forms.CharField(label=u'用户名',max_length=100,
#                              widget=forms.TextInput(
#                                  attrs={'class':'form-control','placeholder':u'用户名',
#                                         'required': '', 'autofocus': ''})
#     )
#     pwd=forms.CharField(label=u'密码',
#                         widget=forms.PasswordInput(
#                             attrs={'class':'form-control','placeholder':u'密码','required': ''})
#

class LoginForm(forms.Form):
    """
    表单登录类
    带自定义验证登录功能
    此类参考beginman，并有改进
    """
    us = forms.CharField(label=u'用户名',max_length=100,widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': u'用户名', 'required': '', 'autofocus': ''}
        ),
    )
    pwd = forms.CharField(label=u'密码',widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': u'密码', 'required': ''}
        )
    )
    auto_login = forms.BooleanField(label=u'记住密码',required=False,
        widget=forms.CheckboxInput(attrs={'value': 1}),
    )

    def clean(self):  #自定义验证功能
        cleaned_data = super(LoginForm, self).clean()
        us = cleaned_data.get('us')
        password = cleaned_data.get('pwd')
        auth_login = cleaned_data.get('auth_login', None)

        if us and password:
            if not User.objects.filter(username=us).exists():
                raise forms.ValidationError(u'该账号不存在')

            self.user_cache = authenticate(username=us, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(u'邮箱或密码错误！')

            elif not self.user_cache.is_active:
                raise forms.ValidationError(u'该帐号已被禁用！')


        if auth_login:      # 如果用户勾选了自动登录
            self.auth_login = True
        else:
            self.auth_login=False

        return self.cleaned_data

    def get_user_id(self):
        """获取用户id"""
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        """获取用户实例"""
        return self.user_cache

    def get_auto_login(self):
        """是否勾选了自动登录"""
        return self.auth_login

    def get_user_is_first(self):
        """获取用户是否是第一次登录"""
        is_first = False
        if self.user_cache and self.user_cache.type == -1:
            is_first = True
            self.user_cache.save()
        return is_first
#下面利用之前定义的模型来创建表单，并选择要显示的字段
class BlogForm(forms.Form):
    """blog后台添加表单类"""
    title=forms.CharField(label=u'标题',max_length=100,
                          widget=forms.TextInput(
                              attrs={'class':'form-control','placeholder':u'标题','required':'',}
                          ))
    cate=forms.CharField(label=u'类型',max_length=100,required=False,
                         widget=forms.TextInput(
                              attrs={'class':'form-control',}
                          ))#博客类型
    is_show=forms.CharField(label=u'加密',max_length=100,required=False,
                            widget=forms.TextInput(
                                attrs={'class':'form-control','placeholder':u'密码'}
                            ))
    # content=forms.CharField(label=u'内容',
    #                         widget=forms.Textarea(
    #                             attrs={'class':'form-control','placeholder':u'内容','required':''}))

    #-----下面为ckeditor富文本编辑器的form（表单）配置--------
    # content = forms.CharField(widget=CKEditorWidget())

    #-----下面为wmd markdown编辑器表单配置-----------
    content=forms.CharField(widget=MarkDownInput())

    # tag=forms.CharField(label=u'标签',max_length=100,
    #                     widget=forms.TextInput(
    #                         attrs={'placeholder':u'标签,以空格隔开','required':''}))

    # class Meta:
    #     model=Blog   #用Blog模型来生成博客后台表单
    #     # fields=['title','is_show','content']#选择模型中要显示的字段


class ChangePwdForm(forms.Form):
    """修改账户密码表单类"""
    oldPwd=forms.CharField(label=u'输入当前密码',max_length=30,
                           widget=forms.PasswordInput(attrs={'class':'form-control','required':''}))
    newPwd=forms.CharField(label=u'输入新密码',max_length=30,
                           widget=forms.PasswordInput(attrs={'class':'form-control','required':''}))

    def clean(self): #自定义验证功能
        cleaned_data = super(ChangePwdForm, self).clean()
        oldPwd=cleaned_data.get('oldPwd')
        if oldPwd:
            user=User.objects.get(username__exact='syz')#获取账户名'syz'对象
            if  not user. check_password(oldPwd):
                raise forms.ValidationError(u'密码输入错误，请重新输入!!!')
        return self.cleaned_data

