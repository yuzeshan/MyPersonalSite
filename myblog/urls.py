#-*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from common.rss import LatestEntriesFeed
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^manage/', include('manager.urls')),      #配置的应用manager的urls，以manger斜杠开头
    url(r'^ckeditor/', include('ckeditor.urls')),  #ckeditor配置
    url(r'^search/', include('haystack.urls')),  #全文搜索

)
urlpatterns += patterns('',
   (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
)
urlpatterns += patterns('myblog.views',
    url(r'^$', 'home', name='home'),   #站点首页
    url(r'^index/$', 'index', name='index'),   #博客列表页面
    # url(r'^blog/search/$','search',name='search'),#博客检索
    url(r'^sideInfo/$','sideInfo',name='sideInfo'),#异步侧边栏的加载，其实就是ajax返回html页面后加载
    url(r"^blog/(?P<pk>\d+)/$",'blog',name='blog'),#博客具体内容页面
    url(r"^category/(?P<pk>\d+)/$",'category',name='category'),#博客分类
    url(r"^blog_tag/(?P<pk>\d+)/$",'blog_tag',name='blog_tag'),#博客标签
    url(r'^ciphertext/(?P<pk>\d+)/$','ciphertext',name='ciphertext'),
    url(r"^pigeonhole/$",'pigeonhole',name='pigeonhole'),#博客归档
    url(r"^login/$",'login_',name='login'),#登录
    url(r"^logout/$",'logout_',name='logout'),#登出
    url(r"^feed/$",LatestEntriesFeed()), #订阅源


    url(r'^wiki/$', 'wiki', name='wiki'),   # 维基内容
    url(r"^wiki_name/(?P<pk>\d+)/$",'wiki_name',name='wiki_name'),#维基名检索
    url(r"^wiki/(?P<pk>\d+)/$",'wiki_con',name='wiki'),#维基名章节内容，注意name要与url相同，而不一定要与view一致


)


