#-*- coding:utf-8 -*-
from django.db import models
from ckeditor.fields import RichTextField
from wmd import models as wmd_models
# Create your models here.
class Category(models.Model):
    """博客类型"""
    name=models.CharField(max_length=40)

    def __unicode__(self):
        return self.name
    class Meta:
        ordering=["id"]

    @models.permalink
    def get_absolute_url(self):
        return ('category',(),{'pk':self.pk})




class Blog(models.Model):
    title=models.CharField(max_length=100)
    img=models.CharField(max_length=500,null=True) #博客导图

    #下面是ckeditor富文本编辑器配置
    # content=RichTextField()
    #下面是wmd markdown编辑器配置
    content=wmd_models.MarkDownField()

    add_date=models.DateTimeField(auto_now_add=True)
    cate=models.ForeignKey(Category)  #博客类型外键
    counts=models.IntegerField(default=0)  #点击率
    is_show=models.CharField(max_length=100,null=True)#博客加密
    class Meta:
        ordering=["-id"]

    def __unicode__(self):
        return self.title


    def getTags(self):
        return Tag.objects.filter(blog=self.pk)  #获取指定id下的博客所有标签

    @models.permalink
    def get_absolute_url(self):
        return ('blog',(),{'pk':self.pk})


class Blog_tag(models.Model):
    """博客标签"""
    name=models.CharField(max_length=100,blank=True)
    add_date=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=["id"]
    def __unicode__(self):
        return self.name
    @models.permalink
    def get_absolute_url(self):
        return ('blog_tag',(),{'pk':self.pk})

class Tag(models.Model):
    blog=models.ForeignKey(Blog)
    tag=models.ForeignKey(Blog_tag)
    def __unicode__(self):
        return self.tag.name





