import logging

from event_bus import BaseConsumerMixin, BaseProducerMixin


class EventBus(BaseConsumerMixin, BaseProducerMixin):
    def __init__(self, host=None, port=None):
        super().__init__(host=host, port=port)
        logging.info('Init event bus')

    def register(self, exchange, exchange_type, consume_key, consume_queue=''):
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.routing_key = consume_key
        self.queue = consume_queue
        super(EventBus, self).start()

        logging.info('Register event bus as thread')

        self.set_on_message_callback(self.get)

    def put(self, queue, dictionary):
        raise NotImplementedError('Method put must be realized')

    def get(self, ch, method, props, body):
        raise NotImplementedError('Method get must be realized')
