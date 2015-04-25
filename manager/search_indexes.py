#-*- coding:utf-8 -*-
from manager.models import Blog,Wiki
from haystack import indexes
class BlogIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    add_date = indexes.DateTimeField(model_attr='add_date')
    def get_model(self):
        return Blog
    def index_queryset(self,using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()   #确定在建立索引时有些记录被索引，这里我们简单地返回所有记录

class WikiIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    add_date = indexes.DateTimeField(model_attr='add_date')
    def get_model(self):
        return Wiki
    def index_queryset(self,using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()   #确定在建立索引时有些记录被索引，这里我们简单地返回所有记录