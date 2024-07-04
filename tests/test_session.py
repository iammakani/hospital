from session import Session

from unittest.mock import patch


# session отвечает за старт сессии и интерактивное распределение команд пользователя между другими конкретными
# методами модулей, поэтому предполагаю, что тут нужна проверка этого правильного распределения
# так же где это возможно осуществить проверку данных с которыми вызваны другие модули (communicator)

@patch('command_handler.CommandHandler.get_status')
@patch('communicator.Communicator.get_command', side_effect=['get status', 'узнать статус пациента'])
def test_start_when_command_is_get_status(_, mock_get_status):
    session = Session()

    session.start(cycles=2)

    assert mock_get_status.call_count == 2


@patch('command_handler.CommandHandler.status_up')
@patch('communicator.Communicator.get_command', side_effect=['status up', 'повысить статус пациента'])
def test_start_when_command_is_status_up(_, mock_status_up):
    session = Session()

    session.start(cycles=2)

    assert mock_status_up.call_count == 2


@patch('command_handler.CommandHandler.status_down')
@patch('communicator.Communicator.get_command', side_effect=['status down', 'понизить статус пациента'])
def test_start_when_command_is_status_up(_, mock_status_down):
    session = Session()

    session.start(cycles=2)

    assert mock_status_down.call_count == 2


@patch('command_handler.CommandHandler.get_statistics')
@patch('communicator.Communicator.get_command', side_effect=['calculate statistics', 'рассчитать статистику'])
def test_start_when_command_is_get_statistics(_, mock_get_statistics):
    session = Session()

    session.start(cycles=2)

    assert mock_get_statistics.call_count == 2


@patch('command_handler.Communicator.send_message')
@patch('communicator.Communicator.get_command', side_effect=['стоп'])
def test_start_when_command_is_stop_ru(_, mock_send_message):
    session = Session()

    session.start()

    assert mock_send_message.called_once_with('Сеанс завершён.')


@patch('command_handler.Communicator.send_message')
@patch('communicator.Communicator.get_command', side_effect=['stop'])
def test_start_when_command_is_stop_eng(_, mock_send_message):
    session = Session()

    session.start()

    assert mock_send_message.called_once_with('Сеанс завершён.')


@patch('command_handler.Communicator.send_message')
@patch('communicator.Communicator.get_command', side_effect=['Qwe', 'get_status', '123', 'exit'])
def test_start_when_command_is_not_valid(_, mock_send_message):
    session = Session()

    session.start(cycles=4)

    mock_send_message.assert_called_with('Неизвестная команда! Попробуйте ещё раз')
    mock_send_message.assert_called_with('Неизвестная команда! Попробуйте ещё раз')
    mock_send_message.assert_called_with('Неизвестная команда! Попробуйте ещё раз')
    mock_send_message.assert_called_with('Неизвестная команда! Попробуйте ещё раз')

    assert mock_send_message.call_count == 4
