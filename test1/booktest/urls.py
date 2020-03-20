from django.conf.urls import url
from booktest import views
# index
# index2
urlpatterns = [
    # 通过 url函数设置url路由配置项
    url(r'^index$', views.index),  #建立/index和index之间的关系
    url(r"^index2$", views.index2),
    url(r"^books$", views.show_books),
    url(r"^books/(\d+)$", views.details),
]