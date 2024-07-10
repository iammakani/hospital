import pytest

from communicator import Communicator2
from errors import IdValueError

from unittest.mock import MagicMock


def test_get_command():
    mock_console = MagicMock()
    communicator2 = Communicator2(console=mock_console)
    mock_console.input = MagicMock(side_effect=['get status', 'STATUS UP', 'РасСЧитАТЬ СтатИСтиКУ'])

    assert communicator2.get_command() == 'get status'
    assert communicator2.get_command() == 'status up'
    assert communicator2.get_command() == 'рассчитать статистику'

    assert mock_console.input.call_count == 3


@pytest.mark.parametrize('command, result', [('get status', 'get status'),
                                             ('STATUS UP', 'status up'),
                                             ('РасСЧитАТЬ СтатИСтиКУ', 'рассчитать статистику')])
def test_get_command_with_parametrize(command, result):
    mock_console = MagicMock()
    communicator2 = Communicator2(console=mock_console)
    mock_console.input = MagicMock(return_value=command)

    assert communicator2.get_command() == result


def test_get_command_prompt():
    mock_console = MagicMock()
    communicator2 = Communicator2(console=mock_console)
    mock_console.input = MagicMock(return_value='get status')

    communicator2.get_command()

    mock_console.input.assert_called_with('Введите команду: ')


def test_get_patient_id():
    mock_console = MagicMock()
    communicator2 = Communicator2(console=mock_console)
    mock_console.input = MagicMock(return_value='2')

    assert communicator2.get_patient_id() == 2


def test_get_patient_id_prompt():
    mock_console = MagicMock()
    communicator2 = Communicator2(console=mock_console)
    mock_console.input = MagicMock(return_value='2')

    communicator2.get_patient_id()

    mock_console.input.assert_called_with('Введите ID пациента: ')


def test_get_patient_id_when_value_is_not_valid():
    mock_console = MagicMock()
    communicator2 = Communicator2(console=mock_console)
    mock_console.input = MagicMock(side_effect=['два', '-1'])

    with pytest.raises(IdValueError):
        communicator2.get_patient_id()

    with pytest.raises(IdValueError):
        communicator2.get_patient_id()

    assert mock_console.input.call_count == 2


def test_will_patient_discharge():
    mock_console = MagicMock()
    communicator2 = Communicator2(console=mock_console)
    mock_console.input = MagicMock(side_effect=['да', 'Да'])

    assert communicator2.will_patient_discharge()
    assert communicator2.will_patient_discharge()

    assert mock_console.input.call_count == 2


def test_will_patient_discharge_prompt():
    mock_console = MagicMock()
    communicator2 = Communicator2(console=mock_console)
    mock_console.input = MagicMock(return_value='да')

    communicator2.will_patient_discharge()

    mock_console.input.assert_called_with('Желаете этого клиента выписать? (да/нет): ')


def test_will_patient_discharge_when_answer_is_not_yes():
    mock_console = MagicMock()
    communicator2 = Communicator2(console=mock_console)
    mock_console.input = MagicMock(side_effect=['нет', 'не нужно', 'yes', 'нужно выписать'])

    assert communicator2.will_patient_discharge() is False
    assert communicator2.will_patient_discharge() is False
    assert communicator2.will_patient_discharge() is False
    assert communicator2.will_patient_discharge() is False

    assert mock_console.input.call_count == 4


@pytest.mark.parametrize('user_answer', ['нет', 'не нужно', 'yes', 'нужно выписать'])
def test_will_patient_discharge_when_answer_is_not_yes_with_parametrize(user_answer):
    mock_console = MagicMock()
    communicator2 = Communicator2(console=mock_console)
    mock_console.input = MagicMock(return_value=user_answer)

    assert communicator2.will_patient_discharge() is False
