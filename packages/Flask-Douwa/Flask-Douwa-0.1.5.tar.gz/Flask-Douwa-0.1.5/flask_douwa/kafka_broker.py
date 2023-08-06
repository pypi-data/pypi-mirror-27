import msgpack
import confluent_kafka

api_version_request = True

class CreateConsumer(object):
    def __init__(self, consumer):
        self.consumer = consumer

    def __enter__(self):
        return self.consumer

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.consumer.close()


def get_last_offset(consumer, topic, partition):
    assig = consumer.assignment()[0]
    lo, hi = consumer.get_watermark_offsets(assig, timeout=1.0)
    # print('Queried offsets for %s: %d - %d' % (assig, lo, hi))
    return confluent_kafka.TopicPartition(topic, offset=hi-1, partition=partition)


def _get_message(consumer):
    message = None

    while True:
        msg = consumer.poll()
        # if msg is not None and msg.error() is not None and msg.error().code() == confluent_kafka.KafkaError._PARTITION_EOF:
        #     break
        if msg is None:
           raise Exception('Got timeout from poll() without a timeout set: %s' % msg)

        if msg.error():
            if msg.error().code() == confluent_kafka.KafkaError._PARTITION_EOF:
                print('Reached end of %s [%d] at offset %d' %
                     (msg.topic(), msg.partition(), msg.offset()))
                break
            else:
                print('Consumer error: %s: ignoring' % msg.error())
                break

        message = msg.value()

        tstype, timestamp = msg.timestamp()
        # print('%s[%d]@%d: key=%s, value=%s, tstype=%d, timestamp=%s' %
        #           (msg.topic(), msg.partition(), msg.offset(),
        #            msg.key(), msg.value(), tstype, timestamp))
    return message


def get_message(conf, topic, pid, callback):

    default_conf = {'group.id': pid,
            'session.timeout.ms': 6000,
            'enable.auto.commit': False,
            'default.topic.config': {
                 'auto.offset.reset': 'earliest'
            }}
    conf.update(default_conf)

    message = None
    value = None
    consumer = confluent_kafka.Consumer(**conf)
    with CreateConsumer(consumer) as c:
        c.subscribe([topic])

        message = _get_message(c)
        if message:
            data = msgpack.loads(message, encoding='utf-8')
            value = callback(c, data)
            # c.commit()

    # return message.decode('utf-8')
    return value


def send_message(conf, topic, message, pid):

        default_conf = {'api.version.request': api_version_request,
                        'default.topic.config': {'produce.offset.report': True}
                        }
        conf.update(default_conf)
        p = confluent_kafka.Producer(**conf)

        try:
            p.produce(topic, value=msgpack.dumps(message, use_bin_type=True), key=pid)
            p.poll(0)
        except BufferError as e:
            print('%% Local producer queue is full (%d messages awaiting delivery): try again\n' %
                            len(p))
        p.flush()


if __name__ == '__main__':
    bootstrap_servers = "kafka-ons-internet.aliyun.com:8080"
    topic = 'ptopic'
    send_message(conf, topic, {"hello":"world"})
    print(get_message(topic))
