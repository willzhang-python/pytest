from django.shortcuts import render, redirect  # 重定向函数
from booktest.models import BookInfo, HeroInfo, AreaInfo
from datetime import date
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.
def index(request):
    """显示图书信息"""
    # 1,查询所有图书的信息
    book_lists = BookInfo.objects.all()

    # 2,模板话html页面返回给浏览器,即调用render函数
    return render(request, "booktest/index.html", {"book_detail": book_lists})


def create(request):
    """新增一本图书"""
    # 1,创建一个bookinfo对象
    c = BookInfo()
    c.bbook = "流星蝴蝶剑"
    c.bpub_date = date(1990, 1, 1)
    # 2,提交
    c.save()
    # 3,返回应答,并且让浏览器再访问/index ,重定向,告诉浏览器去访问下面这个地址
    # return HttpResponse("添加成功")
    # return HttpResponseRedirect("/index")
    return redirect('/index')


def delete(request, bid):
    """删除一本图书"""
    # 传递要删除的图书id
    book = BookInfo.objects.get(id=bid)
    # 删除图书
    book.delete()
    # 重定向,让浏览器重新加载index
    # return HttpResponseRedirect("/index")
    return redirect('/index')


def areas(request):
    """获取广州市的上级地区和下级地区"""
    # 获取城市信息
    area = AreaInfo.objects.get(atitle='广州市')
    # 找到父级地区
    parent = area.aParent
    # 找到下级地区
    children = area.areainfo_set.all()
    # 返回模板数据
    return render(request, 'booktest/areas.html', {'area': area,
                                                   'parent': parent,
                                                   'children': children})
