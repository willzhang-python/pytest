from django.shortcuts import render
from django.http import HttpResponse
from booktest.models import BookInfo, HeroInfo
from django.template import loader, RequestContext

'''
下面这个函数其实就是render这个函数,django已经帮你定义好这个函数,可以直接调用
def my_render(request, templates_path, context_dict={}):
    # 使用模板文件
    # 1,加载模板文件,模板对象
    temp = loader.get_template(templates_path)
    # 2,定义模板上下文:给模板文件传递数据
    context = RequestContext(request, context_dict)
    # 3,模板渲染:产生标准的html内容
    res_html = temp.render(context)
    # 4,返回给浏览器数据
    return HttpResponse(res_html)
'''


# Create your views here.
# 1,定义视图函数,HttpRequest
# 2,进行url配置,建立url地址和试图的对应关系
# http://127.0.0.1:8000/index
def index(request):
    """进行处理,和M和T进行交互"""
    # return HttpResponse("我返回的是index的内容,请知悉.")
    # return my_render(request, "booktest/index.html")
    return render(request, "booktest/index.html", {"content": "hello world", "list": list(range(1, 9))})


# http://127.0.0.1:8000/index2
def index2(request):
    return HttpResponse("我是随便返回的内容!")


def show_books(request):
    # 1,去请求数据库的数据
    books = BookInfo.objects.all()
    # 2,返回模板数据
    return render(request, "booktest/show_books.html", {"books": books})


def details(request, bid):
    # 1,传递过来的是书名的id,要拿到书名id去找英雄的列表
    book = BookInfo.objects.get(id=bid)
    # 2,进行数据表之间的关联
    hero_details = book.heroinfo_set.all()
    # 2,返回模板数据
    return render(request, "booktest/details.html", {"hero_details": hero_details, "books": book})