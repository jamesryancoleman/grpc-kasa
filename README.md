# grpc-kasa

This project demonstrates how to handle requests provided in gRPC for a TP-Link Kasa Smart Plug.

- `bulb.py` provides high level functions to access the plug.
- `parse.py` provides methods for extracting key information from URI
- `device.proto` specifies the grpc interface in the Protocol Buffer language.
- `device_pb2_grpc.py` provides the server stubs.
- `device_pb2.pyi` provices the messages classes used for requests and responses.

### Testing
1. Provide `DEVICE_ADDR` in the `client_test.py` file
2. Start the server in `server.py`
3. Run `client_test.py`