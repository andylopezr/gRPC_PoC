# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: logger_service.proto
# Protobuf Python Version: 5.28.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    1,
    '',
    'logger_service.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14logger_service.proto\"1\n\nLogRequest\x12\x12\n\nevent_type\x18\x01 \x01(\t\x12\x0f\n\x07\x64\x65tails\x18\x02 \x01(\t\"\x1d\n\x0bLogResponse\x12\x0e\n\x06logged\x18\x01 \x01(\x08\x32\x39\n\rLoggerService\x12(\n\x0bLogActivity\x12\x0b.LogRequest\x1a\x0c.LogResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'logger_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_LOGREQUEST']._serialized_start=24
  _globals['_LOGREQUEST']._serialized_end=73
  _globals['_LOGRESPONSE']._serialized_start=75
  _globals['_LOGRESPONSE']._serialized_end=104
  _globals['_LOGGERSERVICE']._serialized_start=106
  _globals['_LOGGERSERVICE']._serialized_end=163
# @@protoc_insertion_point(module_scope)
