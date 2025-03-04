# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import file_service_pb2 as file__service__pb2

GRPC_GENERATED_VERSION = '1.68.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in file_service_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class FileServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SayHello = channel.unary_unary(
                '/file.FileService/SayHello',
                request_serializer=file__service__pb2.HelloRequest.SerializeToString,
                response_deserializer=file__service__pb2.HelloResponse.FromString,
                _registered_method=True)
        self.SayGoodbye = channel.unary_unary(
                '/file.FileService/SayGoodbye',
                request_serializer=file__service__pb2.GoodbyeRequest.SerializeToString,
                response_deserializer=file__service__pb2.GoodbyeResponse.FromString,
                _registered_method=True)
        self.GetServerTime = channel.unary_unary(
                '/file.FileService/GetServerTime',
                request_serializer=file__service__pb2.Empty.SerializeToString,
                response_deserializer=file__service__pb2.TimeResponse.FromString,
                _registered_method=True)
        self.WriteFile = channel.unary_unary(
                '/file.FileService/WriteFile',
                request_serializer=file__service__pb2.FileRequest.SerializeToString,
                response_deserializer=file__service__pb2.FileResponse.FromString,
                _registered_method=True)
        self.GetFilesList = channel.unary_unary(
                '/file.FileService/GetFilesList',
                request_serializer=file__service__pb2.Empty.SerializeToString,
                response_deserializer=file__service__pb2.FilesListResponse.FromString,
                _registered_method=True)


class FileServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SayHello(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SayGoodbye(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetServerTime(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def WriteFile(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetFilesList(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_FileServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SayHello': grpc.unary_unary_rpc_method_handler(
                    servicer.SayHello,
                    request_deserializer=file__service__pb2.HelloRequest.FromString,
                    response_serializer=file__service__pb2.HelloResponse.SerializeToString,
            ),
            'SayGoodbye': grpc.unary_unary_rpc_method_handler(
                    servicer.SayGoodbye,
                    request_deserializer=file__service__pb2.GoodbyeRequest.FromString,
                    response_serializer=file__service__pb2.GoodbyeResponse.SerializeToString,
            ),
            'GetServerTime': grpc.unary_unary_rpc_method_handler(
                    servicer.GetServerTime,
                    request_deserializer=file__service__pb2.Empty.FromString,
                    response_serializer=file__service__pb2.TimeResponse.SerializeToString,
            ),
            'WriteFile': grpc.unary_unary_rpc_method_handler(
                    servicer.WriteFile,
                    request_deserializer=file__service__pb2.FileRequest.FromString,
                    response_serializer=file__service__pb2.FileResponse.SerializeToString,
            ),
            'GetFilesList': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFilesList,
                    request_deserializer=file__service__pb2.Empty.FromString,
                    response_serializer=file__service__pb2.FilesListResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'file.FileService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('file.FileService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class FileService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SayHello(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/file.FileService/SayHello',
            file__service__pb2.HelloRequest.SerializeToString,
            file__service__pb2.HelloResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SayGoodbye(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/file.FileService/SayGoodbye',
            file__service__pb2.GoodbyeRequest.SerializeToString,
            file__service__pb2.GoodbyeResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetServerTime(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/file.FileService/GetServerTime',
            file__service__pb2.Empty.SerializeToString,
            file__service__pb2.TimeResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def WriteFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/file.FileService/WriteFile',
            file__service__pb2.FileRequest.SerializeToString,
            file__service__pb2.FileResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetFilesList(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/file.FileService/GetFilesList',
            file__service__pb2.Empty.SerializeToString,
            file__service__pb2.FilesListResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
