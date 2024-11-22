import time

from client import *
import bulb

GRPC_SERVER = "localhost:50064"
DEVICE_ADDR = "" # this must be filled by the user

def get_test(key:str, addr=GRPC_SERVER):
    resp = Get(key, addr)
    print(key, "->", resp.Value)

def set_test(key:str, value:str, addr=GRPC_SERVER):
    resp = Set(key, value, addr=addr)
    print(key, "<-", resp.Value)

def get_multiple_test(keys:list[str]):
    R : device_pb2.GetMultipleResponse
    R = GetMutiple(keys)
    for resp in R.Responses:
        print("{} -> {}".format(resp.Key, resp.Value))
        if resp.Error > 0 or resp.ErrorMsg:
            print("\terror_code {}: '{}'".format(resp.Error, resp.ErrorMsg))

def set_multiple_test(keys:list[tuple[str, str]]):
    R : device_pb2.SetMultipleResponse
    R = SetMultiple(keys)
    for resp in R.Responses:
        print("{} <- {}".format(resp.Key, resp.Value))
        if not resp.Ok:
            print("\tsuccess={}".format(resp.Ok))
        if resp.Error > 0 or resp.ErrorMsg:
            print("\terror {}: {}".format(resp.Error, resp.ErrorMsg))


if __name__ == "__main__":
    # user DEVICE_ADDR to set the variable in the bulb library
    bulb.addr = DEVICE_ADDR

    # keys are control point addresses encoded in 
    print("== Get tests ==")
    key1 = "kasa://{}/voltage".format(DEVICE_ADDR)
    get_test(key1)
    key2 = "kasa://{}/current".format(DEVICE_ADDR)
    get_test(key2)

    print("== Set tests ==")
    key3 = "kasa://{}/on".format(DEVICE_ADDR)
    set_test(key3, str(True))
    time.sleep(3)
    key4 = "kasa://{}/power".format(DEVICE_ADDR)
    get_test(key4)
    key5 = "kasa://{}/off".format(DEVICE_ADDR)
    set_test(key5, str(True))