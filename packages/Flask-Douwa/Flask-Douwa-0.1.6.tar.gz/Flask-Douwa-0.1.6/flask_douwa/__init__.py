from flask_douwa import routes
from flask_douwa.rpc.generator_id import GeneratorRpc
from flask_douwa.rpc.demo import ProxyGetRpc
from flask_douwa.cache import RedisCache
from collections import namedtuple
import _thread as thread
import json
from flask_douwa import kafka_broker
from functools import wraps

redis = RedisCache()


class Douwa(object):
    client_access = list()

    def __init__(self, app=None):
        self.getid = None
        self.kafka_callback = dict()
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        host =  app.config["GENERATORID_IP"]
        rpc_register = routes.register
        proto = rpc_register(GeneratorRpc)
        self.getid = ProxyGetRpc(host, proto[0], GeneratorRpc.name)
        redis.connect(app.config["REDIS_HOST"], app.config["REDIS_PORT"], app.config["REDIS_DB"])
        Douwa.client_access = app.config.get("ACCESS_TOKEN", list())
        self.consumer_pid = app.config["CONSUMER_PID"]
        # self.producer_pid = app.config["PRODUCER_PID"]
        self.conf = dict()
        self.conf["bootstrap.servers"] =  app.config["KAFKA_HOST"]
        self.conf["ssl.ca.location"] =  app.config["SSL_PATH"]
        self.conf['sasl.username'] = app.config["KAFKA_USERNAME"]
        self.conf['sasl.password'] = app.config["KAFKA_PASSWORD"]
        self.conf['sasl.mechanisms'] = "PLAIN"
        self.conf['security.protocol'] = 'SASL_SSL'
        self.conf['retries'] = app.config["KAFKA_RETRIES"]
        topic = app.config.get("TOPICS", list())
        if topic:
            thread.start_new(kafka_broker.read_notification_from_ceilometer_over_kafka,(self.conf, topic, self.consumer_pid, self.kafka_callback))

    def send_message(self, topic, message):
        kafka_broker.send_message(self.conf, topic, message)

    def generator_id(self):
        if self.getid:
            return self.getid.GeneratorId()
        else:
            raise Exception("没有初始化")

    def bind(self, topic=None):
        def wrapper(func):
            if topic in self.kafka_callback:
                raise AttributeError('有存在的topic')
            elif topic is None or topic == '':
                raise AttributeError('topic不能为空')
            self.kafka_callback[topic] = func

            # @wraps(func)
            # def inner(*args, **kwargs):
            #     return self.get_message(topic, func)
            # return inner
        return wrapper
