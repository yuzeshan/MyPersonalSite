#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response,Http404,HttpResponseRedirect,render
from django.template import RequestContext
from manager.models import *  #导入manager中的全部models
from django.contrib.auth.models import User
# from common.form import loginForm
from common.form import LoginForm
from django.contrib.auth import authenticate,login,logout
import random
#下面防止ajax post出现403错误
from django.views.decorators.csrf import csrf_exempt

def index(request):
    """首页"""
    blogs=Blog.objects.all()
    categories=Category.objects.all()
    hot_blogs=Blog.objects.order_by("-counts")[:15]
    blog_tags=tagsCloud()
    return render_to_response('index.html',
                              {'blogs':blogs,'categories':categories,'hot_blogs':hot_blogs,
                               'blog_tags':blog_tags,'is_blog_view':False},
                              context_instance=RequestContext(request))

def blog(request,pk):
    """博客详细页面"""
    blog=Blog.objects.get(pk=pk)#获取一个博客对象(相当于Blog类的对象)
    if blog.is_show:
        return HttpResponseRedirect('/ciphertext/%s/'%pk)
    categories=Category.objects.all()
    blog.counts+=1
    blog.save()   #这是必须的，否则数据库参数不变化
    pg=get_neighbor(pk)  #获取上下篇博客的id
    return render_to_response('blog.html',
                              {'blog':blog,'categories':categories,'pg':pg,
                               'is_blog_view':True},
                              context_instance=RequestContext(request))

def get_neighbor(id):
    """获取上一篇 下一篇博客id的索引
    这里利用博客列表的id索引，而不是直接利用id
    因为如果，id不连续就不行了
    用索引则没问题
    """
    #获取数据库中博客id列表
    #比如：[1l,2l,5l,6l]
    id=int(id) #因为传过来的id为字符串
    blogs_id=Blog.objects.values_list('id',flat=True).order_by('id')
    blogs_id=list(blogs_id)
    dic={}
    if blogs_id:
        id_index=blogs_id.index(id)  #获取当前文章id在列表中的索引，比如为1，（id为2l）
        pre=0
        nt=0

        if len(blogs_id)>1:
            if id_index==0:#该文章是第一篇
                nt=blogs_id[id_index+1]
            elif id_index==(len(blogs_id)-1):#该文章是最后一篇
                pre=blogs_id[id_index-1]
            else:
                pre=blogs_id[id_index-1]
                nt=blogs_id[id_index+1]
        else:      #就一篇博客
            pre=0
            nt=0
        dic={'pre':pre,'nt':nt}
    return dic


def category(request,pk):
    """相应分类下的文章检索"""
    try:
        cate=Category.objects.get(pk=pk)
    except Category.DoesNotExist:  #如果分类不存在，则引起404错误
        raise Http404
    blogs=cate.blog_set.all()
    categories=Category.objects.all()
    hot_blogs=Blog.objects.order_by("-counts")[:15]
    blog_tags=tagsCloud()
    return render_to_response('index.html',
                              {'cate':cate,'categories':categories,'blogs':blogs,
                               'hot_blogs':hot_blogs,'blog_tags':blog_tags,'is_blog_view':False,'is_category':True},
                              context_instance=RequestContext(request))
# def search(request):
#     """博客检索"""
#     context={}
#     key=request.GET.get('search',None)
#     blogs=Blog.objects.filter(title__icontains=key).order_by('-id')
#     context['key']=key
#     context['blogs']=blogs
#     context['categories']=Category.objects.all()
#     context['hot_blogs']=Blog.objects.order_by("-counts")[:15]
#     context['blog_tags']=tagsCloud()
#     return render_to_response('search.html',context,context_instance=RequestContext(request))

def blog_tag(request,pk):
    """相应标签下的文章检索"""
    blogs=[]
    try:
        blog_tag=Blog_tag.objects.get(pk=pk)
    except Blog_tag.DoesNotExist:  #如果标签不存在，则引起404错误
        raise Http404
    tags=blog_tag.tag_set.all()
    for obj in tags:
        blogs.append(obj.blog)
    categories=Category.objects.all()
    hot_blogs=Blog.objects.order_by("-counts")[:15]
    blog_tags=tagsCloud()
    return render_to_response('index.html',
                              {'blog_tag':blog_tag,'categories':categories,'blogs':blogs,
                               'hot_blogs':hot_blogs,'blog_tags':blog_tags,'is_blog_view':False,'is_blog_tag':True},
                              context_instance=RequestContext(request))

def tagsCloud():
    """标签云"""
    tags = Blog_tag.objects.all()
    tagscloud = []
    for obj in tags:
        size = random.randint(12, 35)        # 随机字体
        R = random.randint(0, 254)
        G = random.randint(0, 254)
        B = random.randint(0,254)       # 没有白色
        RGB = 'rgb(%d,%d,%d)' %(R,G,B)      # 随机颜色
        dic = {}
        dic['name'] = obj.name
        dic['id'] = obj.id
        dic['size'] = size
        dic['rgb'] = RGB
        dic['blog_tag']=obj
        tagscloud.append(dic)
    return tagscloud

def pigeonhole(request):
    """博客归档"""
    blog_values=Blog.objects.values('id','title','add_date').order_by('-add_date')
    counts=len(blog_values)
    #使用set有两个好处：
    #1、就是处理效率大大优于列表；2、可以用来去除海量数据的重复；
    #在下面使用，就是为了一’年月‘来分类归档博客
    #下面即为博客的年月列表
    dates=set([str(i['add_date'].year)+str(i['add_date'].month) for i in blog_values])
    blogs_info=[]
    for i in dates:
        dict={}
        blogs_list=[] #为博客对象列表
        count=0    #为‘年月’归档的博客数量
        dict['ye']=i[:4]+u'年'+i[4:]+u'月'   #‘年月’
        for obj in blog_values:
            if str(obj['add_date'].year)+str(obj['add_date'].month)==i:
               blogs_list.append(Blog.objects.get(id=obj['id']))
               count+=1
        dict['count']=count
        dict['blogs_list']=blogs_list
        dict['counts']=counts
        blogs_info.append(dict) #为包含归档信息的字典列表
        #侧边栏信息
        categories=Category.objects.all()
        hot_blogs=Blog.objects.order_by("-counts")[:15]
        blog_tags=tagsCloud()
    return render_to_response('index.html',
                              {'blogs_info':blogs_info,
                               'counts':counts,
                               'categories':categories,
                               'hot_blogs':hot_blogs,
                               'blog_tags':blog_tags,
                               'is_blog_view':False,
                               'is_pigeonhole_view':True,
                              },
                              context_instance=RequestContext(request))

# def login_(request):
#     """登录账号"""
#     if request.method=='POST':
#         form=loginForm(request.POST)
#         if form.is_valid():
#             username=form.cleaned_data['un']
#             password=form.cleaned_data['pwd']
#             user=User.objects.filter(username__exact=username)#验证账户名是否正确
#             if user:
#                 user_v = authenticate(username=username, password=password)#验证账户名与密码是否正确
#                 if user_v is not None:
#                     if user_v.is_active:      ##该账户是否活跃状态
#                         login(request,user_v) #登录账户名和密码
#                         return HttpResponseRedirect('/')#跳转到首页
#                     else:
#                         form.errors['error']=u'该账号已被禁用！'
#                 else:
#                     form.errors['error']=u'密码不正确！'
#             else:
#                 form.errors['error']=u'用户名不存在！'
#
#
#     else:
#         form=loginForm()
#     return render_to_response('login.html',{'form':form},
#                               context_instance=RequestContext(request))

def login_(request):
    """
    登陆
    此views是登录的另一种方法
    上面那种也可以，只不过两种方法的login.html略有不一样
    """
    #侧边栏信息
    categories=Category.objects.all()
    hot_blogs=Blog.objects.order_by("-counts")[:15]
    blog_tags=tagsCloud()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()      # 获取用户实例
            if user:
                login(request, user)
                if form.get_auto_login():       # set session
                    request.session.set_expiry(None)#设置是否自动登录

                return HttpResponseRedirect('/')


    else:
        form = LoginForm()

    return render_to_response('login.html', {'form':form,
                                             'categories':categories,
                               'hot_blogs':hot_blogs,
                               'blog_tags':blog_tags,},
                              context_instance=RequestContext(request))

def logout_(request):
    """登出/注销"""
    logout(request)
    return HttpResponseRedirect('/')


def ciphertext(request,pk=None):
    """密文重定向处理"""
    blog=Blog.objects.get(pk=pk)
    pwd=blog.is_show   #博文的密码
    if request.method=='POST':
       pwd_form=request.POST.get('pwd',None)
       if pwd==pwd_form:
           categories=Category.objects.all()
           blog.counts+=1
           blog.save()   #这是必须的，否则数据库参数不变化
           pg=get_neighbor(pk)  #获取上下篇博客的id
           return render_to_response('blog.html',
                                  {'blog':blog,'categories':categories,'pg':pg,
                                   'is_blog_view':True},
                                  context_instance=RequestContext(request))


    else:
        return render_to_response('ciphertext.html',
                                  context_instance=RequestContext(request))

@csrf_exempt
def sideInfo(request):
    """异步侧边栏加载
    ajax请求，返回要加载的html页面作为返回的数据"""
    if request.method == 'POST':
        context={}
        #侧边栏信息
        categories=Category.objects.all()
        hot_blogs=Blog.objects.order_by("-counts")[:15]
        blog_tags=tagsCloud()
        context['categories']=categories
        context['hot_blogs']=hot_blogs
        context['blog_tags']=blog_tags
        return render_to_response('sideinfo.html',context,context_instance=RequestContext(request))



def wiki(request):
    """wiki测试"""
    return render_to_response('wiki/wiki.html',context_instance=RequestContext(request))


def gitbook(request,template_name):
    """wiki测试"""
    return render_to_response(template_name)

