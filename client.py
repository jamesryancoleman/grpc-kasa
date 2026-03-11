"""For testing only."""

import common_pb2_grpc
import common_pb2
import grpc

import datetime as dt

GRPC_SERVER = 'localhost:50063'

def Get(keys:list[str], addr=GRPC_SERVER) -> common_pb2.GetResponse:
    responses: common_pb2.GetResponse
    with grpc.insecure_channel(addr) as channel:
        stub = common_pb2_grpc.Dev  (channel)
        responses = stub.Get(common_pb2.GetRequest(Keys=keys))
    return responses

def Set(key_value_pairs:list[tuple[str,str]], addr=GRPC_SERVER) -> common_pb2.SetResponse:
    responses: common_pb2.SetResponse
    with grpc.insecure_channel(addr) as channel:
        stub = common_pb2_grpc.GetSetRunStub(channel)
        responses = stub.Set(
            common_pb2.SetRequest(
                Pairs=[common_pb2.SetPair(Key=t[0], Value=t[1]) for t in key_value_pairs]
            )
        )
    return responses

