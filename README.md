# grpc-kasa

This project demonstrates how to handle requests provided in gRPC for a TP-Link Kasa Smart Plug.

- `bulb.py` provides high level functions to access TP-link products.
- `parse.py` provides methods for extracting information from kasa:// URIs
- `device.proto` specifies the grpc interface in the Protocol Buffer language.
- `device_pb2_grpc.py` provides the server stubs.
- `device_pb2.pyi` provices the messages classes used for requests and responses.

### kasa uri schema


### Testing
1. Provide `DEVICE_ADDR` in the `client_test.py` file
2. Start the server in `server.py`
3. Run `client_test.py`

## Architecture
In openBOS values are accessed on remote devices through a series of reverse proxy servers. The typical flow is:

```
               [system_model]
             rpc     │     rpc         OT_protocol
[client_app] --> [devctrl] --> [driver_1] --> [device_1]
                     │              └-------> [device_2]
                     └-------> [driver_2] --> [device_3]
```

The purpose of this relay architecture is to provide a friendly developer experience where client applications **don't** need to know:
- the internal namespace of openBOS, 
- what drivers must be used to access which points,
- how to use the myriad of OT (operational technology) and IoT protocols needed to talk to specific devices.
- the internal namespace of devices drivers.

**All** that a client app or driver programmer needs to know is the `get` and `set` commands.