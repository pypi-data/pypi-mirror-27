from flask_douwa import routes
from flask_douwa.rpc.generator_id import GeneratorRpc
from flask_douwa.rpc.demo import ProxyGetRpc
from flask_douwa.cache import RedisCache
from collections import namedtuple
import _thread as thread
import json
# from flask_douwa import kafka_broker
from functools import wraps

redis = RedisCache()


class Douwa(object):
    client_access = list()

    def __init__(self, app=None):
        self.getid = None
        self.con = dict()
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        def read_notification_from_ceilometer_over_kafka(host, port, topic):
                conf = {'bootstrap.servers': "{}:{}".format(host, port), 'group.id': "group", 'session.timeout.ms': 6000,
                        'default.topic.config': {'auto.offset.reset': 'earliest'}}
                # conf['stats_cb'] = stats_cb
                c = Consumer(**conf)
                c.subscribe(topic)
                try:
                    while True:
                        msg = c.poll(timeout=1.0)
                        if msg is None:
                            continue
                        if msg.error():
                            if msg.error().code() == KafkaError._PARTITION_EOF:
                                print('%% %s [%d] reached end at offset %d\n' %
                                                 (msg.topic(), msg.partition(), msg.offset()))
                            elif msg.error():
                                raise KafkaException(msg.error())
                        else:
                            print('%% %s [%d] at offset %d with key %s:\n' %
                                             (msg.topic(), msg.partition(), msg.offset(),
                                              str(msg.key())))
                            print(msg.value())
                            #setattr(self.cache, msg.topic(), json.loads(msg.value()))
                            setattr(self.cache, msg.topic(), msg.value())
                        break
                except KeyboardInterrupt:
                    print('%% Aborted by user\n')
                c.close()

        host =  app.config["GENERATORID_IP"]
        rpc_register = routes.register
        proto = rpc_register(GeneratorRpc)
        self.getid = ProxyGetRpc(host, proto[0], GeneratorRpc.name)
        redis.connect(app.config["REDIS_HOST"], app.config["REDIS_PORT"], app.config["REDIS_DB"])
        Douwa.client_access = app.config.get("ACCESS_TOKEN", list())
        topic = app.config.get("TOPIC", list())
        self.cache = namedtuple('cache', topic)
        kafka_host = app.config["KAFKA_HOST"]
        kafka_port = app.config["KAFKA_PORT"]
        self.bootstrap_servers = "{}:{}".format(kafka_host, kafka_port)
        # if topic:
        #     thread.start_new(read_notification_from_ceilometer_over_kafka,(self.kafka_host, self.kafka_port, topic))

    def get_message(self, topic):
        return kafka_broker.get_message(self.bootstrap_servers, topic)

    def send_message(self, topic, message):
        kafka_broker.send_message(self.bootstrap_servers, topic, message)

    def generator_id(self):
        if self.getid:
            return self.getid.GeneratorId()
        else:
            raise Exception("没有初始化")

    def bind(self, topic=None):
        def wrapper(func):
            if topic is None or topic == '':
                raise AttributeError('topic is empty')

            @wraps(func)
            def inner(*args, **kwargs):
                kwargs["message"] = self.get_message(topic)
                return func(*args, **kwargs)
            return inner
        return wrapper
