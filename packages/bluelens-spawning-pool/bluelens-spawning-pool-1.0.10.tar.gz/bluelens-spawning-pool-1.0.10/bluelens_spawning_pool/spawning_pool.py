# coding: utf-8
"""
    bluelens-spawning-pool

    Contact: master@bluehack.net
"""

from __future__ import absolute_import

import redis
import json

REDIS_SERVER = 'bl-mem-store'


class SpawningPool(object):
  def __init__(self):
    self._server_url = REDIS_SERVER
    self._metadata_labels = {}
    self._containers = []

  def setServerUrl(self, url=REDIS_SERVER):
    self._server_url = url

  def setServerPassword(self, password):
    self._server_password = password

  def setApiVersion(self, version):
    self._api_version = version

  def setKind(self, kind):
    self._kind = kind

  def setMetadataName(self, name):
    self._metadata_name = name

  def setMetadataNamespace(self, namespace):
    self._metadata_namespace = namespace

  def addMetadataLabel(self, key, value):
    self._metadata_labels[key] = value

  def createContainer(self):
    container = {}
    container['env'] = []
    return container

  def addContainer(self, container):
    self._containers.append(container)

  def setContainerName(self, container, name):
    container['name'] = name

  def addContainerEnv(self, container, name, value):
    env = {}
    env['name'] = name
    env['value'] = value
    container['env'].append(env)

  def setContainerName(self, container, name):
    container['name'] = name

  def setContainerImagePullPolicy(self, container, policy):
    container['imagePullPolicy'] = policy

  def setContainerImage(self, container, image):
    container['image'] = image

  def setRestartPolicy(self, policy):
    self._restart_policy = policy

  def spawn(self):
    # self._rconn = redis.StrictRedis(self._server_url, port=6379)
    self._rconn = redis.StrictRedis(self._server_url, port=6379, password=self._server_password)
    config = {}

    config['apiVersion'] = self._api_version
    config['kind'] = self._kind

    metadata = {}
    metadata['name'] = self._metadata_name
    metadata['namespace'] = self._metadata_namespace
    metadata['labels'] = self._metadata_labels
    config['metadata'] = metadata

    spec = {}
    spec['containers'] = self._containers
    spec['restartPolicy'] = self._restart_policy
    config['spec'] = spec

    # str_config = self.stringify(config)
    str_config = json.dumps(config)
    print(str_config)
    self._rconn.publish('spawn/create', str_config)

  def stringify(self, dic):
    return str(dic)

  def delete(self, data):
    self._rconn = redis.StrictRedis(self._server_url, port=6379, password=self._server_password)
    self._rconn.publish('spawn/delete', json.dumps(data))





