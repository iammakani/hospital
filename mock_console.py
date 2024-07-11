class MockConsole:

    def __init__(self):
        self._expected_requests_and_responses = []
        self._expected_output_messages = []

    def _get_current_request_and_response(self):
        current_request_and_response = self._expected_requests_and_responses.pop(0)
        current_request = current_request_and_response[0]
        current_response = current_request_and_response[1]
        return current_request, current_response

    def _check_current_message_exists_in_expected_messages(self):
        assert self._expected_output_messages, 'f\nПриложение отправило на вывод больше сообщений, чем ожидалось!'

    def _get_current_message(self):
        current_message = self._expected_output_messages.pop(0)
        return current_message

    def add_expected_request_and_response(self, request, response):
        self._expected_requests_and_responses.append((request, response))

    def input(self, request):
        expected_request, expected_response = self._get_current_request_and_response()

        assert request == expected_request, f'\nActual request: {request}' \
                                            f'\nExpected request: {expected_request}'

        return expected_response

    def add_expected_output_message(self, message):
        self._expected_output_messages.append(message)

    def print(self, message):
        self._check_current_message_exists_in_expected_messages()
        expected_message = self._get_current_message()

        assert message == expected_message, f'\nActual message: {message}\'' \
                                            f'\nExpected message: {expected_message}'

    def verify_all_calls_have_been_made(self):
        remaining_requests_and_responses = len(self._expected_requests_and_responses)
        remaining_messages = len(self._expected_output_messages)

        assert remaining_requests_and_responses == 0 and remaining_messages == 0, \
            f'\nОстались запросы/ответы в очереди: {[req for req in self._expected_requests_and_responses]}' \
            f'\nОстались сообщения в очереди: {[msg for msg in self._expected_output_messages]}'
