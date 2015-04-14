#-*- coding:utf-8 -*-
"""
Django settings for myblog project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gg(-s88)cuc@l0&&crxlk9yb56-cy(4&)dvu!8(yau@2_28-^s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'manager',
    'south',
    # 'ckeditor',#这是富文本编辑器
    'wmd',  #这是wmd markdown编辑器
    'linaro_django_pagination',#文章分页
    'haystack', #这是haystack全文搜索

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'linaro_django_pagination.middleware.PaginationMiddleware',#文章分页中间件
)

TEMPLATE_CONTEXT_PROCESSORS=('django.contrib.auth.context_processors.auth',
 'django.core.context_processors.debug',
 'django.core.context_processors.i18n',
 'django.core.context_processors.media',
 'django.core.context_processors.static',
 'django.core.context_processors.tz',
 'django.contrib.messages.context_processors.messages',
 'django.core.context_processors.request',


)



#ckeditor编辑器配置
# import PIL
# MEDIA_URL = "/media/"
# MEDIA_ROOT = os.path.join(BASE_DIR, "media")
# CKEDITOR_UPLOAD_PATH = "article_images"
# CKEDITOR_IMAGE_BACKEND=PIL
# CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'
# CKEDITOR_CONFIGS = {
#     'default': {
#         'toolbar': (
# 			['div','Source','-','Save','NewPage','Preview','-','Templates'],
# 			['Cut','Copy','Paste','PasteText','PasteFromWord','-','Print','SpellChecker','Scayt'],
# 			['Undo','Redo','-','Find','Replace','-','SelectAll','RemoveFormat'],
# 			['Form','Checkbox','Radio','TextField','Textarea','Select','Button', 'ImageButton','HiddenField'],
# 			['Bold','Italic','Underline','Strike','-','Subscript','Superscript'],
# 			['NumberedList','BulletedList','-','Outdent','Indent','Blockquote'],
# 			['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'],
# 			['Link','Unlink','Anchor'],
# 			['Image','Flash','Table','HorizontalRule','Smiley','SpecialChar','PageBreak'],
# 			['Styles','Format','Font','FontSize'],
# 			['TextColor','BGColor'],
# 			['Maximize','ShowBlocks','-','About', 'pbckcode'],
# 		),
# 	}
# }


#--------wmd markdown编辑器配置------
WMD_SHOW_PREVIEW=True  #显示预览
WMD_ADMIN_SHOW_PREVIEW=True  #admin显示预览
ROOT_URLCONF = 'myblog.urls'
#-------django-haystack全文搜索配置-----
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_cn_backend.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    },
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'#保证实时更新索引

WSGI_APPLICATION = 'myblog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'myblogdb',
        'USER':'root',
        'PASSWORD':'5601259',
        'HOST':'127.0.0.1',
        'PORT':'3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "manager/static"),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'static/').replace('\\','/')

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)





