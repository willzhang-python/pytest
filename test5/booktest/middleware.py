from django.http import HttpResponse


# 这个是专门放中间件的类
class BlockedIPSMiddleware(object):
    '''中间件类'''
    EXCLUDE_IPS = []

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        # 函数调用之前都会调用
        user_ip = request.META['REMOTE_ADDR']
        if user_ip in BlockedIPSMiddleware.EXCLUDE_IPS:
            return HttpResponse('<h1>拒绝您的访问</h1>')


class TestMiddleware(object):
    """中间件类"""
    def __init__(self):
        '''服务器重启后第一次客户端的请求时会调用'''
        print("-----init----")

    def process_request(self, request):
        '''产生request后,url匹配之前会调用这个函数'''
        print('----process-request---')
        # 下面的这个是一个干预,直接返回后,就不会调用其他试图了,直接调用最后的process_response
        # return HttpResponse('process-request')

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        '''url匹配之后,试图函数调用之前调用'''
        print('---process-view---')

    def process_response(self, request, response):
        '''试图函数调用之后,内容返回浏览器之前'''
        print('----process-response---')
        return response


class ExceptionTest1Middleware(object):
    def process_exception(self, request, exception):
        """试图函数发生异常时调用"""
        # 调用顺序是注册在后面的先调用
        print('---process-exception 1 --')
        print(exception)


class ExceptionTest2Middleware(object):
    def process_exception(self, request, exception):
        """试图函数发生异常时调用"""
        print('---process-exception 2 --')