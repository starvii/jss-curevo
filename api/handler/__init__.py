from tornado.web import RequestHandler
from method.logger import default_logger as log


class BaseHandler(RequestHandler):

    @property
    def db(self):
        return self.application.db

    def set_default_headers(self):
        """
        开启 CORS 功能，方便调试
        修改内容类型，防止 XSS
        """
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Content-Type', 'application/json; charset=UTF-8')


# def request_filter(request):
#     """
#     检测 Request header 中是否包含了 Content-Type: application/json
#     并没有什么用，仅作为一个过滤的例子
#     :param request:
#     :return:
#     """
#     ct = None
#     for k, v in request.headers.items():
#         if k.strip().lower() == 'Content-Type'.lower():
#             ct = v
#             break
#     if not ct:
#         log.debug('no Content-Type in request headers.')
#         return False
#     l = ct.split(';')
#     l = set([e.strip().lower() for e in l])
#     if 'application/json' in l:
#         return True
#     else:
#         log.debug('no application/json in Content-Type.')
#         return False


# def json_filter(request_func):
#     """
#     过滤装饰器，如果某个方法未能通过 request_filter 检查，则不执行。
#     :param request_func:
#     :return:
#     """
#     def process(this, *args, **kwargs):
#         if request_filter(this.request):
#             request_func(this, *args, **kwargs)
#     return process
