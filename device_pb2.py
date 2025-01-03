# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: device.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'device.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0c\x64\x65vice.proto\x12\x06\x64\x65vctl\"\"\n\x06Header\x12\x0b\n\x03Src\x18\x01 \x01(\t\x12\x0b\n\x03\x44st\x18\x02 \x01(\t\"9\n\nGetRequest\x12\x1e\n\x06Header\x18\x01 \x01(\x0b\x32\x0e.devctl.Header\x12\x0b\n\x03Key\x18\x02 \x01(\t\"\xda\x01\n\x0bGetResponse\x12#\n\x06Header\x18\x01 \x01(\x0b\x32\x0e.devctl.HeaderH\x00\x88\x01\x01\x12\x0b\n\x03Key\x18\x02 \x01(\t\x12\r\n\x05Value\x18\x03 \x01(\t\x12!\n\x05\x44type\x18\x04 \x01(\x0e\x32\r.devctl.DtypeH\x01\x88\x01\x01\x12$\n\x05\x45rror\x18\x05 \x01(\x0e\x32\x10.devctl.GetErrorH\x02\x88\x01\x01\x12\x15\n\x08\x45rrorMsg\x18\x06 \x01(\tH\x03\x88\x01\x01\x42\t\n\x07_HeaderB\x08\n\x06_DtypeB\x08\n\x06_ErrorB\x0b\n\t_ErrorMsg\"X\n\nSetRequest\x12#\n\x06Header\x18\x01 \x01(\x0b\x32\x0e.devctl.HeaderH\x00\x88\x01\x01\x12\x0b\n\x03Key\x18\x02 \x01(\t\x12\r\n\x05Value\x18\x03 \x01(\tB\t\n\x07_Header\"\xd5\x01\n\x0bSetResponse\x12#\n\x06Header\x18\x01 \x01(\x0b\x32\x0e.devctl.HeaderH\x00\x88\x01\x01\x12\n\n\x02Ok\x18\x02 \x01(\x08\x12\x10\n\x03Key\x18\x03 \x01(\tH\x01\x88\x01\x01\x12\x12\n\x05Value\x18\x04 \x01(\tH\x02\x88\x01\x01\x12$\n\x05\x45rror\x18\x05 \x01(\x0e\x32\x10.devctl.SetErrorH\x03\x88\x01\x01\x12\x15\n\x08\x45rrorMsg\x18\x06 \x01(\tH\x04\x88\x01\x01\x42\t\n\x07_HeaderB\x06\n\x04_KeyB\x08\n\x06_ValueB\x08\n\x06_ErrorB\x0b\n\t_ErrorMsg\"B\n\x12GetMultipleRequest\x12\x1e\n\x06Header\x18\x01 \x01(\x0b\x32\x0e.devctl.Header\x12\x0c\n\x04Keys\x18\x02 \x03(\t\"]\n\x13GetMultipleResponse\x12\x1e\n\x06Header\x18\x01 \x01(\x0b\x32\x0e.devctl.Header\x12&\n\tResponses\x18\x02 \x03(\x0b\x32\x13.devctl.GetResponse\"Z\n\x12SetMultipleRequest\x12\x1e\n\x06Header\x18\x01 \x01(\x0b\x32\x0e.devctl.Header\x12$\n\x08Requests\x18\x02 \x03(\x0b\x32\x12.devctl.SetRequest\"]\n\x13SetMultipleResponse\x12\x1e\n\x06Header\x18\x01 \x01(\x0b\x32\x0e.devctl.Header\x12&\n\tResponses\x18\x02 \x03(\x0b\x32\x13.devctl.SetResponse*\xb7\x01\n\x08GetError\x12\x12\n\x0eGET_ERROR_NONE\x10\x00\x12\x19\n\x15GET_ERROR_UNSPECIFIED\x10\x01\x12 \n\x1cGET_ERROR_KEY_DOES_NOT_EXIST\x10\x02\x12\x15\n\x11GET_ERROR_TIMEOUT\x10\x03\x12&\n\"GET_ERROR_COULD_NOT_RESOLVE_DRIVER\x10\x04\x12\x1b\n\x17GET_ERROR_ACCESS_DENIED\x10\x05*\xf2\x01\n\x08SetError\x12\x12\n\x0eSET_ERROR_NONE\x10\x00\x12\x19\n\x15SET_ERROR_UNSPECIFIED\x10\x01\x12 \n\x1cSET_ERROR_KEY_DOES_NOT_EXIST\x10\x02\x12\x15\n\x11SET_ERROR_TIMEOUT\x10\x03\x12&\n\"SET_ERROR_COULD_NOT_RESOLVE_DRIVER\x10\x04\x12\x1b\n\x17SET_ERROR_ACCESS_DENIED\x10\x05\x12\x17\n\x13SET_ERROR_READ_ONLY\x10\x06\x12 \n\x1cSET_ERROR_INVALID_VALUE_TYPE\x10\x07*\xbb\x01\n\x05\x44type\x12\n\n\x06\x44OUBLE\x10\x00\x12\t\n\x05\x46LOAT\x10\x01\x12\t\n\x05INT32\x10\x02\x12\t\n\x05INT64\x10\x03\x12\n\n\x06UINT32\x10\x04\x12\n\n\x06UINT64\x10\x05\x12\n\n\x06SINT32\x10\x06\x12\n\n\x06SINT64\x10\x07\x12\x0b\n\x07\x46IXED32\x10\x08\x12\x0b\n\x07\x46IXED64\x10\t\x12\x0c\n\x08SFIXED32\x10\n\x12\x0c\n\x08SFIXED64\x10\x0b\x12\x08\n\x04\x42OOL\x10\x0c\x12\n\n\x06STRING\x10\r\x12\t\n\x05\x42YTES\x10\x0e\x32\xfb\x01\n\tGetSetRun\x12.\n\x03Get\x12\x12.devctl.GetRequest\x1a\x13.devctl.GetResponse\x12\x46\n\x0bGetMultiple\x12\x1a.devctl.GetMultipleRequest\x1a\x1b.devctl.GetMultipleResponse\x12.\n\x03Set\x12\x12.devctl.SetRequest\x1a\x13.devctl.SetResponse\x12\x46\n\x0bSetMultiple\x12\x1a.devctl.SetMultipleRequest\x1a\x1b.devctl.SetMultipleResponseB1Z/github.com/jamesryancoleman/bos/services/deviceb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'device_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z/github.com/jamesryancoleman/bos/services/device'
  _globals['_GETERROR']._serialized_start=997
  _globals['_GETERROR']._serialized_end=1180
  _globals['_SETERROR']._serialized_start=1183
  _globals['_SETERROR']._serialized_end=1425
  _globals['_DTYPE']._serialized_start=1428
  _globals['_DTYPE']._serialized_end=1615
  _globals['_HEADER']._serialized_start=24
  _globals['_HEADER']._serialized_end=58
  _globals['_GETREQUEST']._serialized_start=60
  _globals['_GETREQUEST']._serialized_end=117
  _globals['_GETRESPONSE']._serialized_start=120
  _globals['_GETRESPONSE']._serialized_end=338
  _globals['_SETREQUEST']._serialized_start=340
  _globals['_SETREQUEST']._serialized_end=428
  _globals['_SETRESPONSE']._serialized_start=431
  _globals['_SETRESPONSE']._serialized_end=644
  _globals['_GETMULTIPLEREQUEST']._serialized_start=646
  _globals['_GETMULTIPLEREQUEST']._serialized_end=712
  _globals['_GETMULTIPLERESPONSE']._serialized_start=714
  _globals['_GETMULTIPLERESPONSE']._serialized_end=807
  _globals['_SETMULTIPLEREQUEST']._serialized_start=809
  _globals['_SETMULTIPLEREQUEST']._serialized_end=899
  _globals['_SETMULTIPLERESPONSE']._serialized_start=901
  _globals['_SETMULTIPLERESPONSE']._serialized_end=994
  _globals['_GETSETRUN']._serialized_start=1618
  _globals['_GETSETRUN']._serialized_end=1869
# @@protoc_insertion_point(module_scope)
