from concurrent import futures
from enum import StrEnum
from zoneinfo import ZoneInfo
import datetime
import logging
import asyncio

from bospy import common_pb2_grpc
from bospy import common_pb2
import grpc

import parse
import bulb

# this server
SERVER_PORT = "50064"

tz = ZoneInfo('America/New_York')

# Singleton class used to handle Get and Set method calls
class BulbHandler(object):    
    def HandleGet(self, host:str, field:str) -> common_pb2.GetPair:
        bulb.addr = host # override last address
        
        value = None
        dtype:str
        if field == "status":
            value = asyncio.run(bulb.State())
            dtype = common_pb2.BOOL
            print('status', value, dtype)
        elif field == "on":
            value = asyncio.run(bulb.State())
            dtype = common_pb2.BOOL
            print('on', value, dtype)
        elif field == "off":
            value = asyncio.run(bulb.State())
            value = not value
            dtype = common_pb2.BOOL
            print('off', value, dtype)
        elif field == "voltage":
            value = asyncio.run(bulb.Voltage())
            dtype = common_pb2.FLOAT
        elif field == "current":
            value = asyncio.run(bulb.Current())
            dtype = common_pb2.FLOAT
        elif field == "power":
            value = asyncio.run(bulb.Power())
            dtype = common_pb2.FLOAT
        else:
            return common_pb2.GetPair(Error=common_pb2.GET_ERROR_KEY_DOES_NOT_EXIST)
        print("value:", value, type(value))
        return common_pb2.GetPair(Value=str(value), Dtype=dtype)
    
    def HandleSet(self, host:str, field:str, value=None) -> tuple[bool, common_pb2.SetError]:
        bulb.addr = host # override last address

        if field == "status":
            return False, common_pb2.SetError.SET_ERROR_READ_ONLY
        elif field == "on":
            value = ConvertToBool(value)
            # print("value for on() was: ", value)
            if value:
                asyncio.run(bulb.On())
            else:
                asyncio.run(bulb.Off())
            return True, None
        elif field == "off":
            value = ConvertToBool(value)
            # print("value for off() was: ", value)
            if value:
                asyncio.run(bulb.Off())
            else:
                asyncio.run(bulb.On())
            return True, None
        elif field == "voltage":
            return False, common_pb2.SetError.SET_ERROR_READ_ONLY
        elif field == "current":
            return False, common_pb2.SetError.SET_ERROR_READ_ONLY
        elif field == "power":
            return False, common_pb2.SetError.SET_ERROR_READ_ONLY
        else:
            return False, common_pb2.SetError.SET_ERROR_KEY_DOES_NOT_EXIST
        
def ConvertToBool(v:str) -> bool:
    return v.lower() in ("true", "1")

# instantiate singleton
handler = BulbHandler()

# start the gRPC server
class DeviceControlServicer(common_pb2_grpc.DeviceControlServicer):  
    def Get(self, request:common_pb2.GetRequest, context):
        print("received Get request: {}".format(request.Keys))
        header = common_pb2.Header(Src=request.Header.Dst, Dst=request.Header.Src)

        keys = request.Keys
        response_pairs = []
        for k in keys:
            params = parse.KasaParams(k)
            pair = handler.HandleGet(params.host, params.field)
            if pair.Error > 0:
                print("failed to get {} from {}: error code {} ".format(params.field, 
                                                                        params.host,
                                                                        pair.Error))
                response_pairs.append(common_pb2.GetPair(
                    Key=k,
                    # Update to support more errors returned to client
                    Error=common_pb2.GET_ERROR_KEY_DOES_NOT_EXIST,
                    ErrorMsg="Unknown key {}".format(k)))
            else:
                pair.Key = k
                pair.time=datetime.datetime.now(tz)
                response_pairs.append(pair)

        resp = common_pb2.GetResponse(
                    Header=header,
                    Pairs=response_pairs)
        return resp
      
    def Set(self, request:common_pb2.SetRequest, context):
        print("received Set request:")
        for p in request.Pairs:
            print("\t{}: {}".format(p.Key, p.Value))
        header = common_pb2.Header(Src=request.Header.Dst, Dst=request.Header.Src)
        set_responses:list[common_pb2.SetPair] = []
        request_params = [parse.KasaParams(pair.Key) for pair in request.Pairs]
        for i, p in enumerate(request_params):
            value = request.Pairs[i].Value
            ok, err = handler.HandleSet(p.host, p.field, value)
            if not ok:
                print("failed to set {} at {} with {}".format(p.field, p.host, value))
            set_responses.append(common_pb2.SetPair(
                Key=p.url,
                Value=value,
                Ok=ok,
                Error=err,
            ))

        return common_pb2.SetResponse(Header=header, Pairs=set_responses)


if __name__ == "__main__":
    # start the server
    print("== starting server ==")
    
    # run the grpc server
    def serve():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        common_pb2_grpc.add_DeviceControlServicer_to_server(DeviceControlServicer(), server)
        server.add_insecure_port("[::]:" + SERVER_PORT)
        server.start()
        print("== server started, listening on " + SERVER_PORT + " ==")
        server.wait_for_termination()

    logging.basicConfig()
    serve()
