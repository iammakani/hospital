class MockConsole:

    def __init__(self):
        self._expected_requests_and_responses = []
        self._expected_output_messages = []

    def add_expected_request_and_response(self, request, response):
        self._expected_requests_and_responses.append((request, response))

    def input(self, request):
        request_and_response = self._expected_requests_and_responses.pop(0)
        if request_and_response[0] == request:
            return request_and_response[1]
        else:
            raise AssertionError

    def add_expected_output_message(self, message):
        self._expected_output_messages.append(message)

    def print(self, message):
        try:
            expected_output_message = self._expected_output_messages.pop(0)
            if message == expected_output_message:
                return message
            else:
                raise AssertionError
        except IndexError:
            raise AssertionError

    def verify_all_calls_have_been_made(self):
        if len(self._expected_requests_and_responses) > 0 or len(self._expected_output_messages) > 0:
            raise AssertionError
