from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader, RequestContext
from booktest.models import BooInfo
from PIL import Image, ImageDraw, ImageFont
from django.utils.six import BytesIO
from django.core.urlresolvers import reverse


# 写一个装饰器
def login_required(view_func):
    '''登录判断装饰器'''
    def wrapper(request, *view_args, **view_kwargs):
        # 判断用户是否登录
        if request.session.has_key('isLogin'):
            # 用户已登录名,调用对应的视图
            return view_func(request, *view_args, **view_kwargs)
        else:
            # 用户未登录,跳转到登录页
            return redirect('/login')
    return wrapper


def my_render(request, template_path, context={}):
    """服务器处理浏览器请求并返回数据顺序"""
    # 1,加载模板文件
    temp = loader.get_template(template_path)
    # 2,定义模板上下文,给模板文件传递数据
    context = RequestContext(request, context)
    # 3,模板渲染,产生替换后的一个html内容
    res_html = temp.render(context)
    # 4,返回应答
    return HttpResponse(res_html)


# Create your views here.
def index(request):
    """首页"""
    return my_render(request, 'booktest/index.html')


def index2(request):
    """模板文件加载顺序"""
    return render(request, 'booktest/index2.html')


def temp_var(request):
    """测试模板变量传递值"""
    my_dict = {'title': '字典键值'}
    my_list = [1, 2, 3]
    book = BooInfo.objects.get(id=1)
    context = {'my_dict': my_dict, "my_list": my_list, 'book': book}
    return render(request, 'booktest/temp_var.html', context)


def temp_tags(request):
    """模板标签"""
    books = BooInfo.objects.all()
    return render(request, 'booktest/temp_tags.html', {'books': books})


def temp_filter(request):
    """模板过滤器"""
    books = BooInfo.objects.all()
    return render(request, 'booktest/temp_filter.html', {'books': books})


def temp_inherit(request):
    """模板继承"""
    return render(request, 'booktest/child.html')


def html_escape(request):
    """html转义"""
    return render(request, 'booktest/html_escape.html', {'content': '<h1>hello</h1>'})


def login(request):
    # 显示登录页面
    # login_check设置了session来记录用户的登录状态,因此在登录的时候需要先判断是不是登录过
    if request.session.has_key('isLogin'):
        # 用户已登录,直接跳转至修改密码页面
        return redirect('/change_pwd')
    else:
        # 未登录的话就去登录吧!
        # print(request.COOKIES)
        # 第一次登录的时候是不知道有没有cookie的,所以需要确认以下
        # 如果需要在浏览器中记录多个值的话那就需要在login_check中设置多个cookie
        if 'username' in request.COOKIES:
            username = request.COOKIES['username']
        # 多个值时就再加个if判断就行
        # if 'num' in request.COOKIES:
        #     print(request.COOKIES['num'])
        else:
            username = ''
        return render(request, 'booktest/login.html', {'username': username})


def login_check(request):
    # print(type(request.POST))
    # request.POST 保存的是post方式提交的参数 QueryDict格式
    # request.GET 保存的是get方式提交的参数 QueryDict格式
    username = request.POST.get("username")
    password = request.POST.get("password")
    remember = request.POST.get('remember')

    # 获取用户输入的验证码
    vcode1 = request.POST.get("vcode")
    # 获取系统记录的验证码
    # vcode2 = request.session['verifycode']
    vcode2 = request.session.get('verifycode')
    # 两个验证码匹配
    if vcode1 != vcode2:
        redirect('/login')

    # print(remember)
    # print(username+" : " + password)
    # 进行登录的校验
    # 实际开发:根据用户名和密码查找数据库
    # 模拟情况: smart 123
    if username == 'smart' and password == '123':
        # 用户名密码正确,跳转到修改密码页面
        response = redirect('/change_pwd')
        # 在用户名输入正确的前提下,判断是否需要记住用户名,不然判断就没有意义
        if remember == 'on':
            # 设置cookie,需要一个HttpResponse对象,上面的redicect就是这么一个对象,所以可以在此基础上直接设置cookie
            # 设置cookie username ,过期时间1周
            # 设置一个username的cookie,记录的就是用户输入的username
            response.set_cookie("username", username, max_age=7*24*3600)
        # 跳转到首页之后,设置一个session来记录用户的登录状态
        request.session['isLogin'] = True
        # 记住登录的用户名
        request.session['username'] = username
        # 设置过期时间
        request.session.set_expiry(3600)
        return response
    else:
        # 用户名或密码错误,跳转到登录页面
        return redirect('/login')
    # return HttpResponse('ok,收到啦!!')


@login_required
def change_pwd(request):
    """显示修改密码页面"""
    # 首先要进行用户密码的判断
    # 但是一般不会这么做,而是用装饰器来做
    # if not request.session.has_key('isLogin'):
    #     return redirect('/login')
    return render(request, 'booktest/change_pwd.html')


@login_required
def change_pwd_action(request):
    """模拟修改密码处理"""
    # 1,获取新密码
    pwd = request.POST.get('pwd')
    # 2,获取用户名
    username = request.session.get('username')
    # 3,实际开发的哈斯后:修改对应数据库中的数据..
    # 4,返回一个应答
    return HttpResponse("%s修改的密码为%s" % (username, pwd))


def verify_code(request):
    # 引入随机函数模块
    import random
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('FreeMono.ttf', 23)
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    # 内存文件操作
    buf = BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')


def url_reverse(request):
    """url反向解析"""
    return render(request, 'booktest/url_reverse.html')


def show_args(request, a, b):
    return HttpResponse(a + ":" + b)


def show_kwargs(request, c, d):
    return HttpResponse(c + ":" + d)


def test_redirect(request):
    # 重定向到/index
    # return redirect('/index')
    # reverse其实是一个支持反向解析的函数
    # url = reverse('booktest:index')

    # 重定向到/show_args/1/2
    url = reverse('booktest:show_args', args=(1, 2))

    # 重定向到/show_kwargs/3/4
    # url = reverse('booktest:show_kwargs', args={'c': 3, 'd': 4})

    return redirect(url)