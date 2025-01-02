import time

from client import *
import bulb

GRPC_SERVER = "localhost:50064"
DEVICE_ADDR = "192.168.1.186" # this must be filled by the user

def get_test(key:str, addr=GRPC_SERVER):
    resp = Get([key], addr)
    p = resp.Pairs[0]
    print(key, "->", p.Value)

def set_test(key:str, value:str, addr=GRPC_SERVER):
    resp = Set([(key, value)], addr=addr)
    resp = resp.Pairs[0]
    print(key, "<-", resp.Value)

def get_multiple_test(keys:list[str]):
    R : comms_pb2.GetResponse
    R = Get(keys)
    for p in R.Pairs:
        print("{} -> {}".format(p.Key, p.Value))
        if p.Error > 0 or p.ErrorMsg:
            print("\terror_code {}: '{}'".format(p.Error, p.ErrorMsg))

# you need multiple smart plugs to test this.
def set_multiple_test(keys:list[tuple[str, str]]):
    R : comms_pb2.SetResponse
    R = Set(keys)
    for p in R.Pairs:
        print("{} <- {}".format(p.Key, p.Value))
        if not p.Ok:
            print("\tsuccess={}".format(p.Ok))
        if p.Error > 0 or p.ErrorMsg:
            print("\terror {}: {}".format(p.Error, p.ErrorMsg))


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
    time.sleep(5) # needs to be long enough for the current sensors to detect
    key4 = "kasa://{}/power".format(DEVICE_ADDR)
    get_test(key4)
    key5 = "kasa://{}/off".format(DEVICE_ADDR)
    set_test(key5, str(True))