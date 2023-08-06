import json
import msgpack
import confluent_kafka


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
        if msg is None:
            raise Exception('Got timeout from poll() without a timeout set: %s' % msg)

        if msg.error():
            if msg.error().code() == confluent_kafka.KafkaError._PARTITION_EOF:
                # print('Reached end of %s [%d] at offset %d' %
                #       (msg.topic(), msg.partition(), msg.offset()))
                break
            else:
                print('Consumer error: %s: ignoring' % msg.error())
                break

        message = msg.value()

        # tstype, timestamp = msg.timestamp()
        # print('%s[%d]@%d: key=%s, value=%s, tstype=%d, timestamp=%s' %
        #       (msg.topic(), msg.partition(), msg.offset(),
        #        msg.key(), msg.value(), tstype, timestamp))
    return message


def get_message(bootstrap_servers, topic):

    conf = {'bootstrap.servers': bootstrap_servers,
            'group.id': 'test.py',
            'session.timeout.ms': 6000,
            # 'enable.auto.commit': False,
            'default.topic.config': {
                'auto.offset.reset': 'earliest'
            }}
    message = None
    consumer = confluent_kafka.Consumer(**conf)
    with CreateConsumer(consumer) as c:
        c.subscribe([topic])

        message = _get_message(c)
        # Get current assignment
        if message:
            print(message)
        else:
            lastoffset = get_last_offset(c, topic, 0)

    if not message:
        consumer = confluent_kafka.Consumer(**conf)
        with CreateConsumer(consumer) as c:
            c.subscribe([topic])
            c.commit(offsets=[lastoffset], async=True)
            c.assign([lastoffset])
            print(lastoffset)
            message = _get_message(c)
            if message:
                print(message)
            else:
                raise Exception("没有消息")
    # return message.decode('utf-8')
    return msgpack.loads(message, encoding='utf-8')


def send_message(bootstrap_servers, topic, message):
        conf = {'bootstrap.servers': bootstrap_servers}
        p = confluent_kafka.Producer(**conf)

        try:
            p.produce(topic, msgpack.dumps(message, use_bin_type=True))
        except BufferError as e:
            print('%% Local producer queue is full (%d messages awaiting delivery): try again\n' %
                            len(p))
        p.flush()


if __name__ == '__main__':
    bootstrap_servers = "47.100.21.215:32787"
    topic = 'mytopic'
    get_message(bootstrap_servers, topic)
