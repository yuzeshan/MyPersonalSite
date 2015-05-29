#-*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('manager.views',

    url(r'^add/$', 'addBlog',name='add'),      #添加博客
    url(r'^delete/$','deleteBlog',name='delete'), #删除博客
    url(r'^upload/$','uploadBlog',name='upload'), #上传写好的md格式博客
    url(r'^changePwd/$','changePwd',name='changePwd'),# 修改账户密码
    url(r'^add_type/$','addType',name='addType'),#增加类型名称
    url(r'^delType/$','delType',name='delType'),#删除类型
    url(r'^delTag/$','delTag',name='delTag'),#删除标签

    url(r'^addWiki/(?P<pk>\d+)/$', 'addWiki',name='addWiki'),      #添加wiki内容
    url(r'^delWikiName/$','delWikiName',name='delWikiName'),#删除wiki教程
    url(r'^addWikiName/$','addWikiName',name='addWikiName'),#添加wiki名称
    url(r'^delWikiChapter/$','delWikiChapter',name='delWikiChapter'),#删除wiki教程的章节内容

    url(r'^pic/create_type/$','createPicType',name='createPicType'),  #创建图片相册，即图片类型
    url(r'^pic/upload/$', 'UploadPicType', name='UploadPicType'),  #上传图片相册封面图

)