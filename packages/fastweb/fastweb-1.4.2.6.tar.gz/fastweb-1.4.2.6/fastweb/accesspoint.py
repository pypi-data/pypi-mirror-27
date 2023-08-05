# coding:utf8

"""第三方模块接入点"""

import tornado
from tornado.web import UIModule
from tornado import web, iostream
from tornado.ioloop import IOLoop
from tornado.locks import Condition
from tornado.options import options
from tornado.process import Subprocess
from tornado.concurrent import run_on_executor, TracebackFuture
from tornado import gen, web, httpserver, ioloop
from tornado.gen import coroutine, Return, Task, sleep
from tornado.httpclient import HTTPClient, AsyncHTTPClient, HTTPError, HTTPRequest

from kombu import Queue, Exchange
from celery.exceptions import Ignore
from celery import Task as CeleryTask, platforms, Celery, task, states
from celery.schedules import crontab

from thrift.server import TServer
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TCompactProtocol

from subprocess32 import Popen

from docopt import docopt

import pymysql
import tornado_mysql

from zeep import CachingClient
from zeep.exceptions import Error
from zeep.wsse.username import UsernameToken
from zeep.transports import Transport