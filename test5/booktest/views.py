from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# 下面这个是用于创建文件夹的
from django.conf import settings
from booktest.models import PicTest, AreaInfo
# 下面是用于分页的
from django.core.paginator import Paginator


EXCLUDE_IPS = ['127.0.0.1']


def block_ip(func):
    # 使用装饰器来限制ip,这样太麻烦,所以用中间件
    def wrapper(request, *args, **kwargs):
        user_ip = request.META['REMOTE_ADDR']
        if user_ip in EXCLUDE_IPS:
            return HttpResponse('<h1>拒绝您的访问</h1>')
        else:
         return func(request, *args, **kwargs)
    return wrapper


# Create your views here.\
# @block_ip
def static_test(request):
    '''展示静态图片'''
    return render(request, 'booktest/static_test.html')


# @block_ip
def index(request):
    '''首页'''
    # 获取客户端的ip地址
    user_ip = request.META['REMOTE_ADDR']
    print(user_ip)
    # a = 'b' + 1
    return render(request, 'booktest/index.html')


def show_upload(request):
    # 显示上传图片
    return render(request, 'booktest/upload_pic.html')


def upload_handle(request):
    '''上传图片处理'''
    # 1,获取上传文件的处理对象(上传文件必须是post提交)
    pic = request.FILES['pic']
    print(type(pic))
    # 上传的文件小于2.5M的时候,会记录在内存中
    # <class 'django.core.files.uploadedfile.InMemoryUploadedFile'>
    # 上传的文件小于2.5M的时候,会写在临时文件中
    # <class 'django.core.files.uploadedfile.TemporaryUploadedFile'>

    # 获取文件的名称 print(pic.name)

    # 这是一个生成器,每次返回文件的一部分内容,以下可以遍历,读取文件的内容
    print((pic.chunks()))
    # <generator object File.chunks at 0x7f0464114fc0>

    # 2,创建一个文件
    save_path = "%s/booktest/%s" % (settings.MEDIA_ROOT, pic.name)

    # 3,获取上传文件的内容并写到创建的文件中
    with open(save_path, 'wb') as f:
        for content in pic.chunks():
            f.write(content)

    # 4,在数据库中保存上传记录(在数据表中插入记录)
    PicTest.objects.create(goods_pic='booktest/%s' % pic.name)

    # 5,返回
    return HttpResponse('OK')


def show_area(request, pindex):
    '''分页展示地区代码'''
    # 1,获取地区数据
    areas = AreaInfo.objects.filter(aParent__isnull=True)

    # 2,分页,每页显示10条
    paginator = Paginator(areas, 10)
    print(paginator.num_pages)   # 展示总页数
    print(paginator.page_range)  # 展示页码列表

    # 3,获取第pindex页的内容
    if pindex == '':
        # 默认展示第一页的内容
        pindex = 1
    else:
        pindex = int(pindex)
    # paginator是Page类的实例对象(可以获取指定页面的内容)
    page = paginator.page(pindex)

    # 4,使用模板返回数据
    return render(request, 'booktest/show_area.html', {'page': page})


def areas(request):
    '''省市县选中案例'''
    return render(request, 'booktest/areas.html')


def prov(request):
    '''获取所有省级地区的信息'''
    # 1,获取省级地区的信息
    areas = AreaInfo.objects.filter(aParent__isnull=True)

    # 2,拼接json数据:atitle, id(因为获取到的数据对象不是json格式)
    areas_list = []
    for area in areas:
        areas_list.append((area.id, area.atitle))

    # 3,返回数据(json格式数据)
    return JsonResponse({'data': areas_list})


def city(request, pid):
    '''获取市级和县级地区'''
    # 获取pid下级地区的两种方式
    # 1,通过get获取
    # area = AreaInfo.objects.get(pid)
    # areas = area.areainfo_set.all()
    # 2.通过关联查询获取
    areas = AreaInfo.objects.filter(aParent__id=pid)

    # 拼接json数据
    areas_list = []
    for area in areas:
        areas_list.append((area.id, area.atitle))

    # 返回数据
    return JsonResponse({'data': areas_list})
