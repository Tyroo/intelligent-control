from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from jwt.exceptions import ExpiredSignatureError, DecodeError, InvalidTokenError
from app.utils.uart import redis_conn
from django.http import JsonResponse
from app.utils.tools import token_to_username

import jwt


class LoginVerify(MiddlewareMixin):
    # 设置网站访问URL白名单
    white_list = ['/api/LoginApi']

    # 重写父类中的方法，请求之前执行此方法
    def process_request(self, request):
        request_url = request.path_info
        # 当请求url不属于白名单时，验证token是否存在
        if request_url not in self.white_list:
            token = request.META.get('HTTP_X_TOKEN')
            if not token:
                return JsonResponse(status=401,
                                    data={'statusCode': 401, 'redirect': '/Login'},
                                    content_type="application/json")
            try:
                login_user_list = redis_conn.smembers('LOGIN_USER_LIST') or set()
                token_user = token_to_username(token)

                if token_user not in login_user_list:
                    return JsonResponse(status=302,
                                        data={'statusCode': 302, 'redirect': '/Login'},
                                        content_type="application/json")

            except ExpiredSignatureError:
                return JsonResponse(status=302, data={'statusCode': 302, 'redirect': '/Login'},
                                    content_type="application/json")
            except DecodeError:
                return JsonResponse(status=302, data={'statusCode': 302, 'redirect': '/Login'},
                                    content_type="application/json")
            except InvalidTokenError:
                return JsonResponse(status=302, data={'statusCode': 302, 'redirect': '/Login'},
                                    content_type="application/json")
