# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: streaming_service.proto
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
    'streaming_service.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17streaming_service.proto\x12\tstreaming\"\x07\n\x05\x45mpty\"!\n\x0cTimeResponse\x12\x11\n\ttimestamp\x18\x01 \x01(\t\"H\n\tFileChunk\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x12\n\nchunk_data\x18\x02 \x01(\x0c\x12\x15\n\ris_last_chunk\x18\x03 \x01(\x08\"C\n\x0c\x46ileResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x11\n\tfile_path\x18\x03 \x01(\t\"A\n\x0b\x43hatMessage\x12\x0e\n\x06sender\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x11\n\ttimestamp\x18\x03 \x01(\t2\xe0\x01\n\x10StreamingService\x12\x41\n\x10StreamServerTime\x12\x10.streaming.Empty\x1a\x17.streaming.TimeResponse\"\x00\x30\x01\x12\x45\n\x10StreamUploadFile\x12\x14.streaming.FileChunk\x1a\x17.streaming.FileResponse\"\x00(\x01\x12\x42\n\nChatStream\x12\x16.streaming.ChatMessage\x1a\x16.streaming.ChatMessage\"\x00(\x01\x30\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'streaming_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_EMPTY']._serialized_start=38
  _globals['_EMPTY']._serialized_end=45
  _globals['_TIMERESPONSE']._serialized_start=47
  _globals['_TIMERESPONSE']._serialized_end=80
  _globals['_FILECHUNK']._serialized_start=82
  _globals['_FILECHUNK']._serialized_end=154
  _globals['_FILERESPONSE']._serialized_start=156
  _globals['_FILERESPONSE']._serialized_end=223
  _globals['_CHATMESSAGE']._serialized_start=225
  _globals['_CHATMESSAGE']._serialized_end=290
  _globals['_STREAMINGSERVICE']._serialized_start=293
  _globals['_STREAMINGSERVICE']._serialized_end=517
# @@protoc_insertion_point(module_scope)
