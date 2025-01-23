from concurrent import futures
from enum import StrEnum
import logging
import asyncio

import comms_pb2_grpc
import comms_pb2
import grpc

import parse
import bulb

# this server
SERVER_PORT = "50064"

# Singleton class used to handle Get and Set method calls
class BulbHandler(object):    
    def HandleGet(self, host:str, field:str) -> comms_pb2.GetPair:
        bulb.addr = host # override last address
        
        value = None
        dtype:str
        if field == "status":
            value = asyncio.run(bulb.State())
            dtype = comms_pb2.BOOL
        elif field == "on":
            value = asyncio.run(bulb.State())
            dtype = comms_pb2.BOOL
        elif field == "off":
            value = asyncio.run(bulb.State())
            value = not value
            dtype = comms_pb2.BOOL
        elif field == "voltage":
            value = asyncio.run(bulb.Voltage())
            dtype = comms_pb2.FLOAT
        elif field == "current":
            value = asyncio.run(bulb.Current())
            dtype = comms_pb2.FLOAT
        elif field == "power":
            value = asyncio.run(bulb.Power())
            dtype = comms_pb2.FLOAT
        else:
            return comms_pb2.GetPair(Error=comms_pb2.GET_ERROR_KEY_DOES_NOT_EXIST)
        # print("value:", value, type(value))
        return comms_pb2.GetPair(Value=str(value), Dtype=dtype)
    
    def HandleSet(self, host:str, field:str, value=None) -> tuple[bool, comms_pb2.SetError]:
        bulb.addr = host # override last address

        if field == "status":
            return False, comms_pb2.SetError.SET_ERROR_READ_ONLY
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
            return False, comms_pb2.SetError.SET_ERROR_READ_ONLY
        elif field == "current":
            return False, comms_pb2.SetError.SET_ERROR_READ_ONLY
        elif field == "power":
            return False, comms_pb2.SetError.SET_ERROR_READ_ONLY
        else:
            return False, comms_pb2.SetError.SET_ERROR_KEY_DOES_NOT_EXIST
        
def ConvertToBool(v:str) -> bool:
    if v.lower() == "true":
        return True
    return False

# instantiate singleton
handler = BulbHandler()

# start the gRPC server
class GetSetRunServicer(comms_pb2_grpc.GetSetRunServicer):  
    def Get(self, request:comms_pb2.GetRequest, context):
        print("received Get request: {}".format(request.Keys))
        header = comms_pb2.Header(Src=request.Header.Dst, Dst=request.Header.Src)

        keys = request.Keys
        response_pairs = []
        for k in keys:
            params = parse.KasaParams(k)
            pair = handler.HandleGet(params.host, params.field)
            if pair.Error > 0:
                print("failed to get {} from {}: error code {} ".format(params.field, 
                                                                        params.host,
                                                                        pair.Error))
                response_pairs.append(comms_pb2.GetPair(
                    Key=k,
                    # Update to support more errors returned to client
                    Error=comms_pb2.GET_ERROR_KEY_DOES_NOT_EXIST,
                    ErrorMsg="Unknown key {}".format(k)))
            else:
                pair.Key = k
                response_pairs.append(pair)

        resp = comms_pb2.GetResponse(
                    Header=header,
                    Pairs=response_pairs)
        return resp
      
    def Set(self, request:comms_pb2.SetRequest, context):
        print("received Set request:")
        for p in request.Pairs:
            print("\t{}: {}".format(p.Key, p.Value))
        header = comms_pb2.Header(Src=request.Header.Dst, Dst=request.Header.Src)
        set_responses:list[comms_pb2.SetPair] = []
        request_params = [parse.KasaParams(pair.Key) for pair in request.Pairs]
        for i, p in enumerate(request_params):
            value = request.Pairs[i].Value
            ok, err = handler.HandleSet(p.host, p.field, value)
            if not ok:
                print("failed to set {} at {} with {}".format(p.field, p.host, value))
            set_responses.append(comms_pb2.SetPair(
                Key=p.url,
                Value=value,
                Ok=ok,
                Error=err,
            ))

        return comms_pb2.SetResponse(Header=header, Pairs=set_responses)


if __name__ == "__main__":
    # start the server
    print("== starting server ==")
    
    # run the grpc server
    def serve():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        comms_pb2_grpc.add_GetSetRunServicer_to_server(GetSetRunServicer(), server)
        server.add_insecure_port("[::]:" + SERVER_PORT)
        server.start()
        print("== server started, listening on " + SERVER_PORT + " ==")
        server.wait_for_termination()

    logging.basicConfig()
    serve()


        # def Get(self, request:comms_pb2.GetRequest, context):
    #     print("received Get request: key='{}'".format(request.Key))
    #     header = comms_pb2.Header(Src=request.Header.Dst, Dst=request.Header.Src)

    #     # request.Key is of the format "kasa://{HOST}[:PORT]/voltage"
    #     params = parse.KasaParams(request.Key)
    #     value, ok, err = handler.HandleGet(params.host, params.field)
    #     if not ok:
    #         print("failed to get {} from {}: error code {} ".format(params.field, 
    #                                                                 params.host,
    #                                                                 err))
    #         return comms_pb2.GetResponse(
    #             Header=header,
    #             Key=request.Key,
    #             # Update to support more errors returned to client
    #             Error=comms_pb2.GET_ERROR_KEY_DOES_NOT_EXIST,
    #             ErrorMsg="Unknown key {}".format(request.Key),
    #         )        

    #     return comms_pb2.GetResponse(
    #                 Header=header,
    #                 Key=request.Key,
    #                 Value=value,
    #         )