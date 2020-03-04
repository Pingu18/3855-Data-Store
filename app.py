import connexion
from connexion import NoContent

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from request_immediate import RequestImmediate
from request_scheduled import RequestScheduled

import datetime
import requests

import pymysql
import yaml
import json

import pykafka
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread

import logging
from logging import config
from flask_cors import CORS, cross_origin

with open('app_conf.yaml', 'r') as f:
    app_config = yaml.safe_load(f.read())
    host = app_config['datastore']['hostname']
    user = app_config['datastore']['user']
    password = app_config['datastore']['password']
    database = app_config['datastore']['db']
    port = app_config['datastore']['port']

with open('log_conf.yaml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')
logger.setLevel(logging.DEBUG)

DB_ENGINE = create_engine('mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, database))
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

with open('kafka_conf.yaml', 'r') as f:
    app_config = yaml.safe_load(f.read())
    kafka_server = app_config['kafka-conf']['kafka-server']
    kafka_port = app_config['kafka-conf']['kafka-port']
    kafka_topic = app_config['kafka-conf']['kafka-topic']

"""
def request_immediate(requestImmediate):

    session = DB_SESSION()

    ri = RequestImmediate(requestImmediate['name'],
                          requestImmediate['location'],
                          requestImmediate['destination'],
                          requestImmediate['passengers'])

    session.add(ri)

    session.commit()
    session.close()

    return NoContent, 201
"""


def get_request_immediate(startDate=None, endDate=None):
    """ Get immediate ride requests from the data store """

    logger.info("Starting immediate get request")
    startDate = startDate
    endDate = endDate

    if startDate is None or endDate is None:
        logger.debug("Missing date parameter(s)")
        return 'Please supply start date and end date parameters', 400

    results_list = []

    session = DB_SESSION()

    results = []

    logger.info("Querying database")
    results = session.query(RequestImmediate).filter(RequestImmediate.date_created.between(startDate, endDate))

    for result in results:
        results_list.append(result.to_dict())
        print(result.to_dict())

    session.close()
    logger.info("Ending immediate get request")
    return results_list, 200


"""
def request_scheduled(requestScheduled):

    session = DB_SESSION()

    rs = RequestScheduled(requestScheduled['name'],
                          requestScheduled['location'],
                          requestScheduled['destination'],
                          requestScheduled['passengers'],
                          requestScheduled['datetime'])

    session.add(rs)

    session.commit()
    session.close()

    return NoContent, 201
"""


def get_request_scheduled(startDate=None, endDate=None):
    """ Get scheduled ride requests from the data store """

    logger.info("Starting scheduled get request")
    startDate = startDate
    endDate = endDate

    if startDate is None or endDate is None:
        logger.debug("Missing parameter(s)")
        return 'Please supply start date and end date parameters', 400

    results_list = []

    session = DB_SESSION()

    results = []

    logger.info("Querying database")
    results = session.query(RequestScheduled).filter(RequestScheduled.date_created.between(startDate, endDate))

    for result in results:
        results_list.append(result.to_dict())
        print(result.to_dict())

    session.close()
    logger.info("Ending scheduled get request")
    return results_list, 200


def process_messages():
    client = KafkaClient(hosts='{}:{}'.format(kafka_server, kafka_port))
    topic = client.topics['{}'.format(kafka_topic)]
    consumer = topic.get_simple_consumer(
        reset_offset_on_start=False,
        auto_offset_reset=OffsetType.LATEST,
        auto_commit_enable=True,
        auto_commit_interval_ms=1000
    )

    logger.info("Consuming kafka messages")
    consumer.consume()

    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        print('{}'.format(msg))

        session = DB_SESSION()

        data = msg['payload']

        if msg['type'] == "requestImmediate":

            ri = RequestImmediate(data['name'],
                                  data['location'],
                                  data['destination'],
                                  data['passengers'])
            session.add(ri)
            session.commit()
            session.close()

        elif msg['type'] == "requestScheduled":

            rs = RequestScheduled(data['name'],
                                  data['location'],
                                  data['destination'],
                                  data['passengers'],
                                  data['datetime'])
            session.add(rs)
            session.commit()
            session.close()


if __name__ == '__main__':
    app = connexion.FlaskApp(__name__, specification_dir='')
    CORS(app.app)
    app.add_api('openapi.yaml')
    app.app.config['CORS_HEADERS'] = 'Content-Type'
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)
