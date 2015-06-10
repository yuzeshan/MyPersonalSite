#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response,HttpResponseRedirect,HttpResponse
from django.template import RequestContext
from common.form import BlogForm,ChangePwdForm,WikiForm,PicTypeForm
from common.Qiniu import Qiniu
from models import *
from BeautifulSoup import BeautifulSoup
import random
from myblog.views import tagsCloud
import re
import json
from django.contrib.auth.models import User
#下面防止ajax post出现403错误
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def addBlog(request):
    """添加博客"""
    context={}
    tag_obj=Blog_tag.objects.all().order_by('-id')    #以id逆序获得所有标签
    categories=Category.objects.all()
    context['categories']=categories
    context['tags']=tag_obj
    if request.method=='POST':
        form=BlogForm(request.POST)
        if form.is_valid():
            form_data=form.cleaned_data
            title=form_data.get('title')
            is_show=form_data.get('is_show',None)
            cate=form_data.get('cate') #get的是name名
            cate=cate.strip().lower()
            edit_create = int(request.POST.get('edit_or_creat', 0))    # 编辑还是创建
            content=form_data.get('content')
            if edit_create:     # 编辑状态
                blog=Blog.objects.filter(id=edit_create).update(title=title, cate=Category.objects.get(name=cate), content=content, is_show=is_show)
                blog = Blog.objects.get(id=edit_create)
                #将原来添加的标签都删除
                Tag.objects.filter(blog=blog).delete()
            else:
                blog=Blog.objects.create(title=title,cate=Category.objects.get(name=cate),is_show=is_show,content=content)

            # tag=form_data.get('tag')
            # tags=tag.split(" ")#将获取的标签字符串以空格隔开，形成列表
            tags = request.POST.get('mytags', '')
            tags=json.loads(tags)#解析json字符串
            for i in tags:
                if i:
                    if not i in [tag.name for tag in tag_obj]:
                        Blog_tag.objects.create(name=i)
                    #下面是添加标签
                    Tag.objects.create(blog=blog,tag=Blog_tag.objects.filter(name=i)[0])
            #添加博客导图
            img=getBlogPic(blog.content)
            blog.img=img
            blog.save()
            return HttpResponseRedirect('/index/')
        else:
            return render_to_response('manager/addBlog.html',context,
                                      context_instance=RequestContext(request))




    else:
        form=BlogForm()
        context['form']=form
        id=request.GET.get('id',None)#获得url的博客的id值，只有处于编辑状态下，才有
        is_edit=0  #初始化编辑flag，若不为0，则处于编辑状态
        if id:      #处于编辑状态
            is_edit=id
            blog=Blog.objects.get(pk=id)  #获取指定id的博客对象
            form=BlogForm({'title':blog.title,'cate':blog.cate.name,
                           'is_show':blog.is_show,'content':blog.content
                           })  #创建blog的内容表单实例
            has_tags=Tag.objects.filter(blog=blog)  #获取指定博客对象的标签实例
            context['has_tags']=has_tags
            context['form']=form
        context['is_edit']=is_edit



    return render_to_response('manager/addBlog.html',context,
        context_instance=RequestContext(request))


@csrf_exempt
def addType(request):
    """增加类型"""
    data={}
    if request.method=='POST':
        cate=request.POST.get('name',None).strip().lower()
        if cate not in [obj.name for obj in Category.objects.all()]:
            cate_id=Category.objects.create(name=cate).id
            data['data']=cate_id
            return HttpResponse(json.dumps(data))


def getBlogPic(html):
    """获取博客图片"""
    soup = BeautifulSoup(html)
    s = soup.find('img')
    if s:
        return s['src']
    #上面几行代码是为了获取文章内容中嵌入的图片
    #下面是文章之后没图片，而随机选择静态文件中的图片
    return '/static/img/blog/%s.jpg' % (random.choice(range(1, 10)))

@csrf_exempt
def deleteBlog(request):
    """删除博客"""
    if request.method=='POST':
        id=request.POST.get('id',None)
        blog=Blog.objects.filter(pk=id).delete()
        Tag.objects.filter(blog=blog).delete()
        return HttpResponse('ok')

@csrf_exempt
def delType(request):
    """删除类型"""
    data={}
    if request.method=='POST':
        id=request.POST.get('id',None)
        cate=Category.objects.get(id=id).delete() #将指定id的类型删除
        if Blog.objects.filter(cate=cate):
            blog=Blog.objects.filter(cate=cate).delete()   #当然也将依赖该类型的博文也全部删除
            Tag.objects.filter(blog=blog).delete()  #同时也将依赖这些博文的标签中介也删除
        data['cate_id']=id
        return HttpResponse(json.dumps(data))
@csrf_exempt
def delTag(request):
    """删除标签"""
    data={}
    if request.method=='POST':
        id=request.POST.get('id',None)
        tag=Blog_tag.objects.get(id=id).delete() #将指定id的标签删除
        Tag.objects.filter(tag=tag).delete()  #同时也将依赖该标签的标签中介也删除
        data['tag_id']=id
        return HttpResponse(json.dumps(data))
import re
def uploadBlog(request):
    """上传博客
    本地编写md格式的博客上传时，需要注意：
    1、开头写上”title博客标题名“；
    2、然后加上“---”，这是为了是标题和博客内容分开；
    3、本地撰写的博客使用markdown语法，上传上去后，就可以显示markdown格式。
    """
    context={}
    errors=[]
    categories=Category.objects.all().order_by('-id')  #以id逆序获得所有类型
    tag_obj=Blog_tag.objects.all().order_by('-id')    #以id逆序获得所有标签
    context['categories']=categories
    context['tags']=tag_obj
    if request.method=='POST':
        files=request.FILES.get('blog')#获取博客文件
        con=re.split('---',files.read().decode('utf-8'))
        # con=files.read().decode('utf-8').split('---')#将博客内容以‘---’分隔开，事实上就是博客名和博客内容
        head=con[0]
        content=con[1]
        title=re.findall(r'title:.*',head)#在head中寻找title。得到['title:文件名','']
        if title:
            title=title[0].split(':')[1].strip()#取列表第一位，并以'：'分成一个含有两个字符串的列表，取第二个即为文件名
        else:
            title=u'未知的标题'
        cate=request.POST.get('cate','')#获取类型
        # tag=request.POST.get('tag','') #获取标签
        tags = request.POST.get('mytags', '')
        tags=json.loads(tags)#解析json字符串

        if not cate:
            errors.append(u'请输入类型字段...')
        # elif not tag:
        #     errors.append(u'请输入标签...')
        else:
            if not cate in [obj.name for obj in categories]:
                Category.objects.create(name=cate)
            blog=Blog.objects.create(title=title,cate=Category.objects.get(name=cate),content=content)
            # tags=tag.split(" ")#将获取的标签字符串以空格隔开，形成列表
            for i in tags:
                if i:
                    if not i in [tag.name for tag in tag_obj]:
                        Blog_tag.objects.create(name=i)
                    #下面是添加标签
                    Tag.objects.create(blog=blog,tag=Blog_tag.objects.filter(name=i)[0])
            #添加博客导图
            img=getBlogPic(blog.content)
            blog.img=img
            blog.save()
        context['cate']=cate
        # context['tag']=tag
        context['blog']=files
        context['errors']=errors
        if not errors:
            return HttpResponseRedirect('/index/')



    return render_to_response('manager/uploadblog.html',context,
                                  context_instance=RequestContext(request))


def changePwd(request):
    """修改账户密码"""
    context={}
    tag_obj=Blog_tag.objects.all().order_by('-id')    #以id逆序获得所有标签
    context['tags']=tag_obj
    context['form']=ChangePwdForm()
    if request.method=='POST':
        form=ChangePwdForm(request.POST)
        if form.is_valid():
            form_data=form.cleaned_data
            oldPwd=form_data.get('oldPwd')
            newPwd=form_data.get('newPwd')
            user=User.objects.get(username__exact='syz')
            if user.check_password(oldPwd):
                user.set_password(newPwd)
                user.save()
                return HttpResponseRedirect('/')
        context['form'] = form
        return render_to_response('manager/changePwd.html',context,
                              context_instance=RequestContext(request))


    return render_to_response('manager/changePwd.html',context,
                              context_instance=RequestContext(request))


def addWiki(request,pk):
    """添加指定wiki名称下的章节内容(要一一添加章节内容，一个章节对应一个数据表列，一个id)
    标题名格式:#***(一级标题，***为内容),##***(二级标题，***为内容)
    至于，一级标题和二级标题的首字indent则由模板中处理
    """
    context={}
    wiki_names=Wiki_Name.objects.all()      #获取所有wiki列表
    wiki_name=Wiki_Name.objects.get(pk=pk)  #获取wiki名称对象
    wikis=wiki_name.wiki_set.all() .order_by('id')         #获取该wiki名称下的所有wiki内容
    context['wiki_names']=wiki_names
    context['wiki_name']=wiki_name
    context['wikis']=wikis
    if request.method=='POST':
        form=WikiForm(request.POST)
        if form.is_valid():
            form_data=form.cleaned_data
            chapter=form_data.get('chapter')#获取章节标题
            content=form_data.get('content')#获取章节内容
            edit = int(request.POST.get('edit', 0))    # 编辑还是创建
            if edit:     # 编辑状态
                Wiki.objects.filter(id=edit).update(name=wiki_name,chapter=chapter,content=content)
            else:
                wiki=Wiki.objects.create(name=wiki_name,chapter=chapter,content=content)

            return HttpResponseRedirect('/wiki/')
        else:
            return render_to_response('manager/addWiki.html',context,
        context_instance=RequestContext(request))


    else:
        form=WikiForm()
        context['form']=form
        id=request.GET.get('id',None)#获得url的wiki章节内容的id值，只有处于编辑状态下，才有
        edit=0  #初始化编辑flag，若不为0，则处于编辑状态
        if id:      #处于编辑状态
            edit=id
            wikichapter=Wiki.objects.get(pk=id)  #获取指定id的博客对象
            form=WikiForm({'chapter':wikichapter.chapter,'content':wikichapter.content})  #创建wiki章节内容表单实例
            context['form']=form
        context['edit']=edit

    return render_to_response('manager/addWiki.html',context,
        context_instance=RequestContext(request))

@csrf_exempt
def delWikiName(request):
    """删除wiki教程"""
    data={}
    if request.method=='POST':
        id=request.POST.get('id',None)
        wiki_name=Wiki_Name.objects.get(id=id).delete() #将指定id的wiki名称删除
        Wiki.objects.filter(name=wiki_name).delete()  #同时也将依赖该wiki名称的章节内容也删除
        data['id']=id
        return HttpResponse(json.dumps(data))

@csrf_exempt
def addWikiName(request):
    """后台添加wiki名称
       同时自动添加img模型字段
    """
    data={}
    if request.method=='POST':
        wikiName=request.POST.get('name',None).strip().lower()
        if wikiName not in [obj.name for obj in Wiki_Name.objects.all()]:
            WikiName=Wiki_Name.objects.create(name=wikiName)
            img=getWikiPic()
            WikiName.img=img
            WikiName.save()
            data['id']=WikiName.id
            return HttpResponse(json.dumps(data))


def getWikiPic():
    """获取wiki名称背景图片"""
    #随机选择静态文件中的图片
    return '/static/img/wiki_name/%s.jpg' % (random.choice(range(1, 4)))

@csrf_exempt
def delWikiChapter(request):
    """删除wiki教程的章节内容
    """
    data={}
    if request.method=='POST':
        id=request.POST.get('id',None)
        Wiki.objects.get(id=id).delete() #将指定id的wiki章节内容删除
        data['id']=id
        return HttpResponse(json.dumps(data))


@csrf_exempt
def UploadPicType(request):
    """上传图片封面图
       将其上传到七牛云上面，并返回url
    """
    if request.method == 'POST':
        img = request.FILES.get('Filedata', None)
        type = request.POST.get('type', None)
        if type:
            qn = Qiniu(img, w=800, h=520)
        else:
            qn = Qiniu(img)
        qn.uploadFile()
        remote_url = qn.downloadFile()
        key = qn.getKey()
        return HttpResponse(json.dumps({'url':remote_url, 'key':key}))


def createPicType(request):
    """创建图片相册，即图片类型"""
    context={}

    if request.method=='POST':
        img=request.POST.get('img',None)
        form = PicTypeForm(request.POST)
        if form.is_valid():
            form_data=form.cleaned_data
            title=form_data.get('title')#获取图片相册标题
            desc=form_data.get('desc',None)#获取图片相册描述
            is_show=form_data.get('is_show',None)#获取图片相册加密密码
            edit=int(request.POST.get('edit',None))
            if edit:
                PicType.objects.filter(pk=edit).update(title=title,desc=desc,img=img,is_show=is_show)
            else:
                PicType.objects.create(title=title,desc=desc,img=img,is_show=is_show)
            return HttpResponseRedirect('/pic/')
        context['form'] = form
    else:
        id=int(request.GET.get('id',0))
        edit=0 #初始化编辑值，若为0，则不是编辑状态
        context['form']=PicTypeForm()
        if id:
            edit=id
            pictype=PicType.objects.get(pk=id)
            form = PicTypeForm({'title':pictype.title,'desc':pictype.desc,'is_show':pictype.is_show})
            context['form']=form
            context['pictype']=pictype
        context['edit']=edit
    return render_to_response('picture/addtype.html',context,
                              context_instance=RequestContext(request))
@csrf_exempt
def uploadPic(request,pk):
    """上传图片相册具体的图片"""
    context={}
    pictype=PicType.objects.get(pk=pk)#获取图片相册类型
    context['pictype'] = pictype
    if request.method == 'POST':    #前台通过ajax来将填写的数据传到后台
        data = request.POST.get('data')
        data = json.loads(data)
        for obj in data:
            Pic.objects.create(type=pictype, img=obj['url'], desc=obj['desc'])
        return HttpResponse('ok')

    return render_to_response('picture/addpic.html', context,
                              context_instance=RequestContext(request))
@csrf_exempt
def delPic(request):
    """ajax删除图片相册或单个图片
       同时将远端的七牛云上的图片也删除
    """

    #这里有个问题，之前设计model的时候没想到
    #删除远端图片的时候需要key，但是model里面没有存，所以下面使通过截取图片url中的key来实现删除的

    if request.method=='POST':
        str_model=request.POST.get('model',None)#获取要删除的类型字符串，例如，如果是pictype，就是要删除相册
        id=request.POST.get('id',None)#获取模型的id值
        if str_model=='pictype':  #删除图片相册，并且将相册中的相片全部删除，包括远端七牛云上
            pictype=PicType.objects.get(pk=id)
            qn = Qiniu(pictype.img[(pictype.img).find('/',7)+1:]) #将远端的图片删除，参数是img链接的key，这里是从字符串38开始，就不计算了
            qn.delFile()
            pics=Pic.objects.filter(type=pictype)#获取图片相册对应的所有图片
            keys=[]   #取得所有图片的key
            for pic in pics:
                keys.append(pic.img[(pic.img).find('/',7)+1:])
            qn = Qiniu(keys)
            qn.delMoreFiles() #删除远端多个图片
            #这两个放到最后再删除，原因是先把pictype删除后，后面就取不到pictype实例，进而取不到pic实例
            pics.delete()  #将图片相册对应的图片也删除
            pictype.delete()#将图片相册删除
            return HttpResponse(json.dumps({'id':id,'model':'pictype'}))
        elif str_model=='pic':
            pic=Pic.objects.get(pk=id)
            qn = Qiniu(pic.img[(pic.img).find('/',7)+1:]) #将远端的图片删除，参数是img链接的key，这里是从字符串38开始，就不计算了
            qn.delFile()
            pic.delete()
            return HttpResponse(json.dumps({'id':id,'model':'pic'}))
@csrf_exempt
def editSave(request):
    """前端编辑图片描述内容。通过ajax保存"""
    if request.method=='POST':
        desc=request.POST.get('desc')
        id=request.POST.get('id')
        pic=Pic.objects.filter(pk=id).update(desc=desc)
        return HttpResponse(json.dumps({'desc':desc}))
















