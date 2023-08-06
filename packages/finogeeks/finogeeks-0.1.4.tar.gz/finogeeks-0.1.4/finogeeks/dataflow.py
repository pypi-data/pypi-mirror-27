"""
author: created by zhao.guangyao on 11/30/17.
desc: 
"""
import os
import datetime
import pymongo
import hashlib
import gridfs
import json
from bson import ObjectId
from kafka import KafkaConsumer, KafkaProducer

import sys
import logging.config
formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
ch = logging.StreamHandler(stream=sys.stderr)
ch.setFormatter(formatter)
log_level = getattr(logging, os.getenv('LOG', 'INFO').upper(), logging.INFO)
logging.basicConfig(level=log_level)


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.addHandler(ch)
    logger.propagate = False
    return logger


class PubSub(object):
    def __init__(self, pipe=None, db='dataflow'):
        self.pipelines = os.getenv(
            'PIPELINES',
            'collector,'
            'downloader,'
            'text_extractor,'
            'date_extractor,'
            'number_extractor,'
            'department_extractor,'
        )
        self.pipelines = [p.strip() for p in self.pipelines.split(',') if p]
        self.idx_pipelines = {p: i for i, p in enumerate(self.pipelines)}
        if pipe.endswith('.py'):
            pipe = pipe[:-3]
        self.pipe = pipe
        self.logger = get_logger(str(self.pipe))

        self.pre_pipe = None
        if self.idx_pipelines[self.pipe] > 0:
            self.pre_pipe = self.pipelines[self.idx_pipelines[self.pipe] - 1]

        self.mq = os.getenv('KAFKA', None)
        self.producer = None
        self.consumer = None
        if self.mq:
            self.producer = KafkaProducer(bootstrap_servers=self.mq)
            if self.pre_pipe:
                self.consumer = KafkaConsumer(self.pre_pipe, bootstrap_servers=self.mq)

        self.skr = Sinker(db)

    @staticmethod
    def r2s(msg):
        return '{:<s} {:<5s} {:<50s} {:<s}'.format(msg['id'], msg.get('url_type', ' '), msg['title'], msg['url'])

    def pub(self, message=None, topic=None):
        if not topic:
            topic = self.pipe
        inserted = self.skr.sink(topic, message)
        if inserted:
            self.logger.info('Pub to {:s}, {:s}'.format(topic, self.r2s(message)))
        if inserted and self.mq:
            if message.get('content', None):
                message['content'] = str(message['content'])
            self.producer.send(topic, json.dumps(message, ensure_ascii=False).encode('utf8'))

    def sub(self, bfr=False, ftr=None, topic=None):
        if not topic and self.pre_pipe:
            topic = self.pre_pipe
        if not self.mq:
            for r in self.skr.load(topic, ftr, bfr):
                self.logger.info('Sub from {:s}, {:s}'.format(topic, self.r2s(r)))
                yield r
        else:
            for r in self.consumer:
                r = json.loads(r.value.decode('utf8'))
                if r.get('content', None):
                    r['content'] = ObjectId(r['content'])
                if bfr:
                    self.skr.load_buffer(r)
                self.logger.info('Sub from {:s}, {:s}'.format(topic, self.r2s(r)))
                yield r

    def query(self, message, topic=None):
        if self.pipe:
            topic = self.pipe
        return self.skr.query(topic, message)

    def close(self):
        self.skr.close()
        if self.producer:
            self.producer.close()
        if self.consumer:
            self.consumer.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class Sinker(object):
    def __init__(self, db='dataflow'):
        mgo_url = os.getenv('MONGO', 'mongodb://127.0.0.1:27017')
        self.cli = pymongo.MongoClient(mgo_url)
        self.db = db
        self.gfs = gridfs.GridFS(self.cli[self.db])

    def sink(self, topic, message):
        if self.query(topic, message):
            return False
        bfr = message.pop('buffer', None)
        if isinstance(bfr, str):
            bfr = bfr.encode('utf8')
        if bfr and not message.get('content', None):
            fn = '{:s}_{:s}'.format(topic, message['id'])
            f = self.gfs.find_one({"filename": fn})
            if f:
                message['content'] = f._id
            else:
                fid = self.gfs.put(bfr, filename=fn)
                message['content'] = fid
        self.cli[self.db][topic].insert_one(message)
        message.pop('_id', None)
        return True

    def query(self, topic, message):
        if 'id' not in message:
            message['id'] = hashlib.md5(message['url'].encode('utf8')).hexdigest()
        if 'release_date' not in message:
            message['release_date'] = ''
        if 'parent' not in message:
            message['parent'] = ''
        if 'spider' not in message:
            message['spider'] = ''
        if 'create_date' not in message:
            message['create_date'] = (
                    datetime.datetime.utcnow()
                    + datetime.timedelta(hours=8)
            ).strftime('%Y-%m-%d %H:%M:%S')

        message['cid'] = hashlib.md5('_'.join([
            message.get('id', ''),
            message.get('spider', ''),
            message.get('category', ''),
            message.get('parent', ''),
        ]).encode('utf8')).hexdigest()
        return self.cli[self.db][topic].find_one({'cid': message['cid']})

    def load(self, topic, ftr=None, bfr=False):
        for r in self.cli[self.db][topic].find(ftr):
            if bfr:
                self.load_buffer(r)
            r.pop('_id', None)
            yield r

    def load_buffer(self, r):
        if r.get('content', None):
            obj = self.gfs.get(r['content'])
            r['buffer'] = obj.read()
            if not obj.filename.startswith('downloader_'):
                r['buffer'] = r['buffer'].decode()
        r.pop('_id', None)
        return r

    def close(self):
        self.cli.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
