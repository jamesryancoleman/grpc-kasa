from concurrent import futures
from enum import StrEnum
import logging
import asyncio

import device_pb2_grpc
import device_pb2
import grpc

import parse
import bulb

# this server
SERVER_PORT = "50064"

# Singleton class used to handle Get and Set method calls
class BulbHandler(object):    
    def HandleGet(self, host:str, field:str) -> tuple[str, bool, device_pb2.GetError]:
        bulb.addr = host # override last address
        
        value:str
        if field == "status":
            value = asyncio.run(bulb.State())
        elif field == "on":
            value = asyncio.run(bulb.State())
        elif field == "off":
            value = asyncio.run(bulb.State())
            value = not value
        elif field == "voltage":
            value = asyncio.run(bulb.Voltage())
        elif field == "current":
            value = asyncio.run(bulb.Current())
        elif field == "power":
            value = asyncio.run(bulb.Power())
        else:
            return value, False, device_pb2.GetError.GET_ERROR_KEY_DOES_NOT_EXIST
        return str(value), True, None
    
    def HandleSet(self, host:str, field:str, value=None) -> tuple[bool, device_pb2.SetError]:
        bulb.addr = host # override last address

        if field == "status":
            return False, device_pb2.SetError.SET_ERROR_READ_ONLY
        elif field == "on":
            print("value for on() was: ", value)
            asyncio.run(bulb.On())
            return True, None
        elif field == "off":
            print("value for off() was: ", value)
            asyncio.run(bulb.Off())
            return True, None
        elif field == "voltage":
            return False, device_pb2.SetError.SET_ERROR_READ_ONLY
        elif field == "current":
            return False, device_pb2.SetError.SET_ERROR_READ_ONLY
        elif field == "power":
            return False, device_pb2.SetError.SET_ERROR_READ_ONLY
        else:
            return False, device_pb2.SetError.SET_ERROR_KEY_DOES_NOT_EXIST

# instantiate singleton
handler = BulbHandler()

# start the gRPC server
class GetSetRunServicer(device_pb2_grpc.GetSetRunServicer):
    def Get(self, request:device_pb2.GetRequest, context):
        print("received Get request: key='{}'".format(request.Key))
        header = device_pb2.Header(Src=request.Header.Dst, Dst=request.Header.Src)

        # request.Key is of the format "kasa://{HOST}[:PORT]/voltage"
        params = parse.KasaParams(request.Key)
        value, ok, err = handler.HandleGet(params.host, params.field)
        if not ok:
            print("failed to get {} from {}: error code {} ".format(params.field, 
                                                                    params.host,
                                                                    err))
            return device_pb2.GetResponse(
                Header=header,
                Key=request.Key,
                # Update to support more errors returned to client
                Error=device_pb2.GET_ERROR_KEY_DOES_NOT_EXIST,
                ErrorMsg="Unknown key {}".format(request.Key),
            )        

        return device_pb2.GetResponse(
                    Header=header,
                    Key=request.Key,
                    Value=value,
            )

    def Set(self, request:device_pb2.SetRequest, context):
        print("received Set request: key={} value={}".format(request.Key, request.Value))
        header = device_pb2.Header(Src=request.Header.Dst, Dst=request.Header.Src)

        params = parse.KasaParams(request.Key)
        ok, err = handler.HandleSet(params.host, params.field, request.Value)
        if not ok:
            print("failed to set {} at {} with {}".format(params.field, 
                                                          params.host,
                                                          request.Value))
            return device_pb2.GetResponse(
                Header=header,
                Key=request.Key,
                # Update to support more errors returned to client
                Error=err,
                ErrorMsg="Unknown key",
            )  

        return device_pb2.SetResponse(
            Header=header,
            Key=request.Key,
            Ok=ok
        )
    
    def GetMultiple(self, request:device_pb2.GetMultipleRequest, context):
        print("received GetMultiple request: keys={}".format(request.Keys))
        header = device_pb2.Header(Src=request.Header.Dst, Dst=request.Header.Src)

        keys = request.Keys
        responses = []
        for k in keys:
            # request.Key is of the format "kasa://{HOST}[:PORT]/voltage"
            params = parse.KasaParams(k)
            value, ok, err = handler.HandleGet(params.host, params.field)
            if not ok:
                print("failed to get {} from {}: error code {} ".format(params.field, 
                                                                        params.host,
                                                                        err))
                responses.append(device_pb2.GetResponse(
                    Header=header,
                    Key=k,
                    # Update to support more errors returned to client
                    Error=device_pb2.GET_ERROR_KEY_DOES_NOT_EXIST,
                    ErrorMsg="Unknown key {}".format(request.Key)))
            else:
                responses.append(device_pb2.GetResponse(
                    Header=header,
                    Key=k,
                    Value=value))

        return device_pb2.GetMultipleResponse(
                    Header=header,
                    Responses=responses,
            )   

if __name__ == "__main__":
    # start the server
    print("== starting server ==")
    
    # run the grpc server
    def serve():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        device_pb2_grpc.add_GetSetRunServicer_to_server(GetSetRunServicer(), server)
        server.add_insecure_port("[::]:" + SERVER_PORT)
        server.start()
        print("== server started, listening on " + SERVER_PORT + " ==")
        server.wait_for_termination()

    logging.basicConfig()
    serve()