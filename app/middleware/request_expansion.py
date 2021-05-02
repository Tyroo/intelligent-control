#!/usr/bin/env python
# -*- coding:utf8 -*-
# __author__ = '北方姆Q'
from django.http import QueryDict

try:
    from django.utils.deprecation import MiddlewareMixin  # 1.10.x
except ImportError:
    MiddlewareMixin = object                # 1.4.x-1.9.x


class HttpPost2HttpOtherMiddleware(MiddlewareMixin):
    """
    可以继续添加HEAD、PATCH、OPTIONS以及自定义方法
    HTTP_X_METHODOVERRIDE貌似是以前版本的key？？？
    :param request: 经过原生中间件处理过后的请求
    :return:
    """
    def process_request(self, request):
        try:
            http_method = request.META['REQUEST_METHOD']
            if http_method.upper() not in ('GET', 'POST'):
                setattr(request, http_method.upper(), QueryDict(request.body))
        except Exception:
            pass
        finally:
            return