from django.conf.urls import url
from booktest import views


urlpatterns = [
    url(r'^static_test$', views.static_test),  # 展示静态图片
    url(r'^index$', views.index),  # 首页
    url(r'^show_upload$', views.show_upload),  # 展示图片上传
    url(r'^upload_handle$', views.upload_handle),  # 图片上传处理
    # 刚刚在处理时,我掐面加上了/,导致浏览器记住了我的设置,所以每次访问都自动加上了/,清一下缓存就可以
    url(r'^show_area(?P<pindex>\d*)$', views.show_area),  # 分页
    url(r'^areas$', views.areas),  # 展示省级地区
    url(r'^prov$', views.prov),  # ajax请求省级地区
    url(r'^city(\d+)$', views.city),  # ajax请求市级县级地区
    url(r'^dis(\d+)$', views.city),  # ajax请求县级级地区
]
