#-*- coding:utf-8 -*-
"""实现wiki章节列表
   一级标题和二级标题的缩进
"""
from django import template
register = template.Library()  #自定义filter时必须加上


@register.filter  #注册template filter
def chapterindent(value):
    if value.find('#')!=-1:
        return value.strip().replace('#','')
    elif value.find('##')!=-1:
        return value.strip().replace('##','123')
    else:
        return value.strip()
