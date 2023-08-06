# coding: utf-8

from __future__ import absolute_import

import os
import grpc
import numpy as np

from .grpc import vector_search_pb2
from .grpc import vector_search_pb2_grpc

VECTOR_SEARCH_HOST = os.environ['VECTOR_SEARCH_HOST']
VECTOR_SEARCH_PORT = os.environ['VECTOR_SEARCH_PORT']

class VectorSearch(object):
  def __init__(self):
    print('init')

  def search(self, vector, limit=10):
    channel = grpc.insecure_channel(VECTOR_SEARCH_HOST + ':' + VECTOR_SEARCH_PORT)
    stub = vector_search_pb2_grpc.SearchStub(channel)
    # v = np.asarray(vector, dtype=np.float32)
    # results = stub.SearchVector(vector_search_pb2.SearchRequest(vector=v.tobytes(),
    #                                                             candidate=limit))
    result = stub.SearchVector(vector_search_pb2.SearchRequest(vector=vector,
                                                                candidate=limit))
    return result.vector_d, result.vector_i

