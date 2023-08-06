# coding:utf8

from urllib.parse import unquote

from fastweb.accesspoint import requests


class HttpClient(object):
    """同步的http访问客户端"""

    @staticmethod
    def fetch(request):
        method = request.method.lower()
        url = request.url

        if method == 'get':
            response = requests.get(url)
        elif method == 'post':
            data = unquote(request.body.decode())
            response = requests.post(url, data=data)

        return response


if __name__ == '__main__':
    from fastweb.component.request import Request

    r = Request(method='POST', url='http://www.baidu.com', body={'k':'v'})
    print(HttpClient.fetch(r))