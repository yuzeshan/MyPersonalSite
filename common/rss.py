#-*- coding:utf-8 -*-
from manager.models import Blog
from django.contrib.syndication.views import Feed
class LatestEntriesFeed(Feed):
    title = u"Shanyuze的博客文章"            # title
    link = "http://yuzeshan.cn/"    #首页链接,还要修改
    author_name='Shanyuze'
    description = u"学习python、django和前端Html&css&js等web开发，并关注大数据、云计算相关互联网态势。。。"
    def items(self):
        """订阅的5篇文章列表"""
        return Blog.objects.order_by('-add_date')[:5]       # 订阅最新5篇
    def item_title(self, item):
        """文章名字"""
        return item.title

    def item_link(self, item):
        """文章链接"""
        return item.get_absolute_url()

    def item_pubdate(self, item):
        """文章发表日期"""
        return item.add_date
    def item_categories(self, item):
        """文章类别"""
        return  (item.cate.name, )
    def item_author_name(self):
        return u"Shanyuze"

