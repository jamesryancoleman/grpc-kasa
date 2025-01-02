import comms_pb2_grpc
import comms_pb2
import grpc

import datetime as dt

GRPC_SERVER = 'localhost:50063'

def Get(keys:list[str], addr=GRPC_SERVER) -> comms_pb2.GetResponse:
    responses: comms_pb2.GetResponse
    with grpc.insecure_channel(addr) as channel:
        stub = comms_pb2_grpc.GetSetRunStub(channel)
        responses = stub.Get(comms_pb2.GetRequest(Keys=keys))
    return responses

def Set(key_value_pairs:list[tuple[str,str]], addr=GRPC_SERVER) -> comms_pb2.SetResponse:
    responses: comms_pb2.SetResponse
    with grpc.insecure_channel(addr) as channel:
        stub = comms_pb2_grpc.GetSetRunStub(channel)
        responses = stub.Set(
            comms_pb2.SetRequest(
                Pairs=[comms_pb2.Pair(Key=t[0], Value=t[1]) for t in key_value_pairs]
            )
        )
    return responses

