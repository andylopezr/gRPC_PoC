from abc import ABC, abstractmethod

class LoggerProvider(ABC):

    @abstractmethod
    def log_activity(self, event_type, details, time_stamp):
        pass

class SQLiteLoggerProvider(LoggerProvider):

    def log_activity(self, event_type, details, time_stamp):
        print('Calling DB')


class CMDLoggerProvider(LoggerProvider):
    def log_activity(self, event_type, details, time_stamp):
        print('Sending to CMD')