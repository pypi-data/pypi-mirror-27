import logging
import asyncio

from event_bus import BaseConsumerMixin, BaseProducerMixin


class EchoEventBus(BaseConsumerMixin, BaseProducerMixin):
    def __init__(self, host=None, port=None):
        super().__init__(host=host, port=port)

        logging.info('Init event bus')
        self._service_meta_info = None
        self.repeater = None

    @property
    def service_meta_info(self):
        return self._service_meta_info

    @service_meta_info.setter
    def service_meta_info(self, value):
        if isinstance(value, dict):
            self._service_meta_info = value
        else:
            raise ValueError('Service meta info must be dictionary')

    def register(self, exchange, exchange_type, consume_key, repeater, **kwargs):
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.routing_key = consume_key
        self.repeater = repeater
        self.queue = ''
        self.service_meta_info = kwargs

        logging.info('Register echo event bus as thread')

        self.set_on_message_callback(self.get)
        super(EchoEventBus, self).start()
        if self.repeater:
            self.put(self.repeater, self.service_meta_info)

    def put(self, queue, dictionary):
        self.push_to_queue(queue, dictionary)

    def get(self, ch, method, props, body):
        logging.info('New topic message {} {}'.format(method, body))

    async def idle(self, idle_time):
        while True:
            await asyncio.sleep(idle_time)
            try:
                self.put(self.repeater, self.service_meta_info)
            except AttributeError as e:
                logging.error(e)
