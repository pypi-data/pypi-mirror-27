# This code is inspired by the code found at, in order to provide
# an implementation with the new cluster architecture provided by
# redis 3:
#   https://github.com/SPSCommerce/redlock-py

import json
import logging
import random
import time
import uuid

import redis
import rediscluster
from rome.conf.configuration import get_config
from rome.core.utils import merge_dicts as merge_dicts


class ClusterLock(object):

    def __init__(self):
        self.retry_count = 1
        self.lock_labels = map(lambda x: "%i" % (x), range(0, 1))
        self.uuid = str(uuid.uuid1())
        config = get_config()
        if config.redis_cluster_enabled():
            startup_nodes = map(
                lambda x: {"host": x,
                           "port": "%s" % (config.port())},
                config.cluster_nodes())
            self.redis_client = rediscluster.StrictRedisCluster(
                startup_nodes=startup_nodes,
                decode_responses=True)
        else:
            self.redis_client = redis.StrictRedis(host=config.host(),
                                                  port=config.port(),
                                                  db=0)

    def lock(self, name, ttl):
        """
        Acquire a lock.
        :param name: a lock name
        :param ttl: time to live
        :return: a boolean value that is True if the lock has been aquired and False in the other
        case.
        """
        self.unlock(name, only_expired=True)
        retry = 0
        request_uuid = ("%s_%s" % (self.uuid, name)).__hash__()
        while retry < self.retry_count:
            now = time.time()
            failed = False
            keys = map(lambda x: "%s_%s" % (x, name), self.lock_labels)
            lock_value = {
                "host": self.uuid,
                "start_date": now,
                "ttl": ttl,
                "request_uuid": request_uuid
            }
            processed_keys = []
            for key in keys:
                lock_value_with_key = merge_dicts(lock_value, {"key": key})
                result = self.redis_client.hsetnx(
                    "lock", key, json.dumps(lock_value_with_key))
                if result == 0:
                    failed = True
                    break
                else:
                    processed_keys += [key]
            if failed:
                self.redis_client.hdel("lock", processed_keys)
                retry += 1
                time.sleep(random.uniform(0.005, 0.010))
            else:
                return True
        return False

    def unlock(self, name, only_expired=False):
        """
        Release a lock.
        :param name: a lock name
        :param only_expired: a boolean. When it is True, the lock is released only if the lock has
        expired.
        :return: a boolean which is True if the lock has been correctly released, and which is False
        in the other case
        """
        request_uuid = ("%s_%s" % (self.uuid, name)).__hash__()
        now = time.time()
        keys = map(lambda x: "%s_%s" % (x, name), self.lock_labels)
        data = self.redis_client.hmget("lock", keys)
        keys_to_delete = []
        for each in data:
            if each:
                json_object = json.loads(each)
                expiration_date = json_object["start_date"] + (
                    json_object["ttl"] / 1000.0)
                if not only_expired:
                    if json_object["request_uuid"] == request_uuid:
                        keys_to_delete += [json_object["key"]]
                if expiration_date < now:
                    keys_to_delete += [json_object["key"]]
                else:
                    logging.debug("still %s ms to wait" %
                                  (expiration_date - now))
        for key in keys_to_delete:
            self.redis_client.hdel("lock", key)
        return True
