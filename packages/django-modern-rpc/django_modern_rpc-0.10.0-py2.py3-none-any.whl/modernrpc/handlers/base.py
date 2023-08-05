# coding: utf-8
from modernrpc.exceptions import RPCInvalidRequest


class RPCHandler(object):

    protocol = None

    def __init__(self, request, entry_point):
        self.request = request
        self.entry_point = entry_point

    def loads(self, str_data):
        """Convert serialized string data to valid Python data, depending on current handler protocol"""
        raise NotImplementedError("You must override loads()")

    def dumps(self, obj):
        """Convert Python data to serialized form, according to current handler protocol."""
        raise NotImplementedError("You must override dumps()")

    @staticmethod
    def valid_content_types():
        raise NotImplementedError("You must override valid_content_types()")

    def can_handle(self):
        # Get the content-type header from incoming request. Method differs depending on current Django version
        try:
            # Django >= 1.10
            content_type = self.request.content_type
        except AttributeError:
            # Django up to 1.9
            content_type = self.request.META['CONTENT_TYPE']

        if not content_type:
            # We don't accept a request with missing Content-Type request
            raise RPCInvalidRequest('Missing header: Content-Type')

        return content_type.lower() in self.valid_content_types()

    def process_request(self):
        """
        Parse self.request to extract payload. Parse it to retrieve RPC call information, and
        execute the corresponding RPC Method. At any time, raise an exception when detecting error.
        :return: The result of RPC Method execution
        """
        raise NotImplementedError("You must override process_request()")

    def result_success(self, data):
        """Return a HttpResponse instance containing the result payload for the given data"""
        raise NotImplementedError("You must override result_success()")

    def result_error(self, exception, http_response_cls=None):
        """Return a HttpResponse instance containing the result payload for the given exception"""
        raise NotImplementedError("You must override result_error()")
