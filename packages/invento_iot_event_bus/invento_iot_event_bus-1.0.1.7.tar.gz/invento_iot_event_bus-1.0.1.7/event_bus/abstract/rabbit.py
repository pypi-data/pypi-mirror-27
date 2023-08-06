import json
import logging
import threading

import pika as pika


class BaseRabbit(threading.Thread):
    DIRECT = 'direct'
    TOPIC = 'topic'
    FANOUT = 'fanout'

    def __init__(self, protocol='amqp', host=None, port=None, creds=None):
        super(BaseRabbit, self).__init__()
        self._exchange = None
        self._exchange_type = self.DIRECT
        self._routing_key = None
        self._queue = None
        self._connection = None
        self._connection_string = '{}://guest:guest@{}:{}/'.format(protocol, host, port)
        self._channel = None

    @property
    def exchange(self):
        return self._exchange

    @exchange.setter
    def exchange(self, value):
        self._exchange = value

    @property
    def exchange_type(self):
        return self._exchange_type

    @exchange_type.setter
    def exchange_type(self, value):
        self._exchange_type = value

    @property
    def routing_key(self):
        return self._routing_key

    @routing_key.setter
    def routing_key(self, value):
        self._routing_key = value

    @property
    def queue(self):
        return self._queue

    @queue.setter
    def queue(self, value):
        self._queue = value

    def connect(self):
        return pika.SelectConnection(parameters=pika.URLParameters(self._connection_string),
                                     on_open_callback=self.on_open, on_close_callback=self.on_connection_closed)

    def run(self):
        raise NotImplementedError('Method run must be implemented')

    def on_open(self, unused_connection):
        raise NotImplementedError('Method run must be implemented')

    def on_connection_closed(self, connection, reply_code, reply_text):
        raise NotImplementedError('Method on_connection_closed must be implemented')

    def on_open_callback(self, channel):
        raise NotImplementedError('Method on_open_callback must be implemented')

    def on_declare_queue(self, me):
        raise NotImplementedError('Method on_declare_queue must be implemented')

    def on_bindok(self, unused_frame):
        raise NotImplementedError('Method on_bindok must be implemented')

    def __reconnect(self):
        raise NotImplementedError('Method __reconnect must be implemented')


class BaseConsumerMixin(BaseRabbit):

    def __init__(self, host, port):
        super(BaseConsumerMixin, self).__init__(host=host, port=port)
        self._connection = None
        self._channel = None
        self.callback_queue = None
        self._consumer_tag = None
        self.__on_message_callback = None
        self.consumer = None

    def run(self):
        self._connection = self.connect()
        self.consumer = self._connection
        self._connection.ioloop.start()

    def set_on_message_callback(self, callback):
        logging.info('Setting message callback as {}'.format(callback.__str__))
        self.__on_message_callback = callback

    def on_open_callback(self, channel):
        channel.exchange_declare(exchange=self.exchange,
                                 exchange_type=self.exchange_type)
        channel.queue_declare(self.on_declare_queue, queue=self._queue, passive=False)
        channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_open(self, channel):
        channel.queue_declare(self.on_declare_queue, queue=self._queue, passive=False)
        channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reply_code, reply_text):
        self._connection.close()

    def on_connection_closed(self, connection, reply_code, reply_text):
        self._channel = None
        logging.warning('Connection closed, reopening in 1 seconds: (%s) %s',
                        reply_code, reply_text)
        self.__reconnect()

    def __reconnect(self):
        logging.warning('Reconnect consumer')
        self._connection.ioloop.stop()
        self._connection = self.connect()
        self._connection.ioloop.start()

    def on_declare_queue(self, me):
        logging.info('Enable exchange')
        self._channel.queue_bind(self.on_bindok, self._queue,
                                 self._exchange, self._routing_key, )

    def on_bindok(self, unused_frame):
        self._consumer_tag = self._channel.basic_consume(self.on_message,
                                                         self._queue,
                                                         no_ack=True)

    def on_open(self, unused_connection):
        self._channel = self._connection.channel(self.on_open_callback)

    def on_message(self, ch, method, props, body):
        logging.info('Call on_message callback')
        return self.__on_message_callback(ch, method, props, body)


class BaseProducerMixin(BaseRabbit):

    def __init__(self, host, port):
        super(BaseProducerMixin, self).__init__(host=host, port=port)
        self._connection = None
        self._channel = None
        self.callback_queue = None
        self._consumer_tag = None
        self.producer = None

    def run(self):
        self._connection = self.connect()
        self.producer = self._connection

    def __reconnect(self):
        self._connection = self.connect()

    def push_to_queue(self, queue, dictionary):
        assert isinstance(dictionary, dict), 'Sending data must be dict'
        try:
            self._channel.basic_publish(exchange=self._exchange,
                                        routing_key=queue,
                                        body=json.dumps(dictionary))
        except Exception as e:
            logging.error('Error while push to queue', e)
