from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timedelta


# request就是httprequest类型的对象
# request包含浏览器请求的信息
# Create your views here.
def index(request):
    """首页"""
    # num = 'a'+1
    # 请求的方式和路径
    print(request.method)
    print(request.path)
    return render(request, 'booktest/index.html')


def showarg(request, num):
    return HttpResponse(num)


def login(request):
    # 显示登录页面
    # login_check设置了session来记录用户的登录状态,因此在登录的时候需要先判断是不是登录过
    if request.session.has_key('isLogin'):
        # 用户已登录,直接跳转至首页
        return redirect('/index')
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
    # print(remember)
    # print(username+" : " + password)
    # 进行登录的校验
    # 实际开发:根据用户名和密码查找数据库
    # 模拟情况: smart 123
    if username == 'smart' and password == '123':
        # 用户名密码正确,跳转到首页
        response = redirect('/index')
        # 在用户名输入正确的前提下,判断是否需要记住用户名,不然判断就没有意义
        if remember == 'on':
            # 设置cookie,需要一个HttpResponse对象,上面的redicect就是这么一个对象,所以可以在此基础上直接设置cookie
            # 设置cookie username ,过期时间1周
            # 设置一个username的cookie,记录的就是用户输入的username
            response.set_cookie("username", username, max_age=7*24*3600)
        # 跳转到首页之后,设置一个session来记录用户的登录状态
        request.session['isLogin'] = True
        # 设置过期时间
        request.session.set_expiry(3600)
        return response
    else:
        # 用户名或密码错误,跳转到登录页面
        return redirect('/login')
    # return HttpResponse('ok,收到啦!!')


# /test_ajax
def ajax_test(request):
    """显示ajax页面"""
    return render(request, 'booktest/test_ajax.html')


def ajax_handle(request):
    """ajax请求处理
    ajax在补充新加载页面的情况下,对页面进行局部的刷新
    """
    # num = 1 + 'a'
    return JsonResponse({'res': 1})


# /login_ajax_
def login_ajax(request):
    """显示ajax登录页面"""
    return render(request, 'booktest/login_ajax.html')


# /login_ajax_check
def login_ajax_check(request):
    """ajax----post登录请求帐号密码校验"""
    username = request.POST.get("username")
    password = request.POST.get("password")
    if username == 'smart' and password == '123':
        # 注意这里不能用render重定向去指定页面,因为是ajax请求
        return JsonResponse({'res': 1})
    else:
        return JsonResponse({'res': 0})


def set_cookie(request):
    """设置网站cookie信息"""
    # 下面的这个设置cookie时需要一个HttpResponse,这个'设置cookie'是返回给浏览器展示的内容
    response = HttpResponse('设置cookie')
    # 设置一个cookie信息,名字为num,值为1
    response.set_cookie('num', 1, max_age=14*24*3600)
    # response.set_cookie('num', 1, expires=datetime.now()+timedelta(days=14))   两周之后过期
    # 返回response
    return response


def get_cookie(request):
    """获取cookie的信息"""
    # 取出cookie num的值
    num = request.COOKIES['num']
    return HttpResponse(num)


def set_session(request):
    """设置session"""
    request.session['username'] = 'smart'
    request.session['age'] = '18'
    #  默认过期时间是两周,但是可以设置
    # request.session.set_expiry(5)
    return HttpResponse('设置session')


def get_session(request):
    """获取session"""
    username = request.session['username']
    age = request.session['age']
    return HttpResponse(username + ":" + str(age))


def clear_session(request):
    """清楚session信息"""
    # request.session.clear()
    request.session.flush()
    return HttpResponse("清楚成功")