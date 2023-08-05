# -*- coding: utf-8 -*-
import time
import datetime
from . import logging
from celery_connectors.utils import ev
from celery_connectors.logging.setup_logging import setup_logging
from celery_connectors.kombu_subscriber import KombuSubscriber
from celery_connectors.publisher import Publisher

setup_logging()


class MessageProcessor:

    def __init__(self,
                 name="message-processor",
                 sub_auth_url=ev("SUB_BROKER_URL", "redis://localhost:6379/0"),
                 sub_ssl_options={},
                 pub_auth_url=ev("PUB_BROKER_URL", "redis://localhost:6379/0"),
                 pub_ssl_options={}):

        self.name = name
        self.log = logging.getLogger(self.name)
        self.recv_msgs = []
        self.sub_auth_url = sub_auth_url
        self.pub_auth_url = pub_auth_url
        self.sub_ssl_options = sub_ssl_options
        self.pub_ssl_options = pub_ssl_options

        self.sub = None
        self.pub = None

        self.exchange = None
        self.exchange_name = ""
        self.queue = None
        self.queue_name = ""
        self.routing_key = None

    # end of __init__

    def process_message(self, body, message):
        log.info(("{} kombu.subscriber recv msg props={} body={}")
                 .format(self.name, message, body))
        self.recv_msgs.append(body)
        message.ack()
    # end of process_message

    def get_pub(self):
        if not self.pub:
            self.pub = Publisher("msg-pub",
                                 self.pub_auth_url,
                                 self.pub_ssl_options)
        return self.pub
    # end of get_pub

    def get_sub(self):
        if not self.sub:
            self.sub = KombuSubscriber("msg-sub",
                                       self.sub_auth_url,
                                       self.sub_ssl_options)
        return self.sub
    # end of get_sub

    def consume_queue(self,
                      queue,
                      exchange,
                      routing_key=None,
                      heartbeat=60,
                      expiration=None,
                      serializer="application/json",
                      seconds_to_consume=10.0,
                      forever=True):

        self.queue_name = queue
        self.exchange_name = exchange
        self.routing_key = routing_key

        self.log(("{} START - consume_queue={} rk={}")
                 .format(self.name,
                         self.queue_name,
                         self.routing_key))

        not_done = True
        while not_done:

            seconds_to_consume = 10.0
            heartbeat = 60
            serializer = "application/json"
            queue = "reporting.accounts"
            sub.consume(callback=self.process_message,
                        queue=self.queue_name,
                        exchange=None,
                        routing_key=None,
                        serializer=serializer,
                        heartbeat=heartbeat,
                        time_to_wait=seconds_to_consume)

            if not forever:
                not_done = False
            # if not forever

        # end of while loop

        self.log(("{} DONE - consume_queue={} rk={}")
                 .format(self.name,
                         self.queue_name,
                         self.routing_key))

    # end of consume_queue

# end of MessageProcessor
