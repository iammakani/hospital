import pytest

from communicator import Communicator
from errors import IdValueError

from unittest.mock import patch
from io import StringIO


@patch('builtins.input', side_effect=['get status', 'STATUS UP', 'РассчиТАТЬ СТАТИстику'])
def test_get_command(mock_input):
    communicator = Communicator()

    assert communicator.get_command() == 'get status'
    assert communicator.get_command() == 'status up'
    assert communicator.get_command() == 'рассчитать статистику'
    assert mock_input.call_count == 3


@pytest.mark.parametrize("command, result", [('get status', 'get status'),
                                             ('STATUS UP', 'status up'),
                                             ('РассчиТАТЬ СТАТИстику', 'рассчитать статистику')])
def test_get_command_with_parametrize(command, result):
    communicator = Communicator()

    with patch('builtins.input', return_value=command):
        assert communicator.get_command() == result


@patch('sys.stdout', new_callable=StringIO)
def test_get_command_prompt(mock_prompt):
    communicator = Communicator()

    with patch('sys.stdin', StringIO('Get Status')):
        communicator.get_command()

    assert mock_prompt.getvalue() == 'Введите команду: '


@patch('builtins.input', return_value='2')
def test_get_patient_id(_):
    communicator = Communicator()

    result = communicator.get_patient_id()

    assert result == 2


@patch('sys.stdout', new_callable=StringIO)
def test_get_patient_id_prompt(mock_prompt):
    communicator = Communicator()

    with patch('sys.stdin', StringIO('2')):
        communicator.get_patient_id()

    assert mock_prompt.getvalue() == 'Введите ID пациента: '


@patch('builtins.input', side_effect=['два', '-1'])
def test_get_patient_id_when_value_is_not_valid(mock_input):
    communicator = Communicator()

    with pytest.raises(IdValueError):
        communicator.get_patient_id()

    with pytest.raises(IdValueError):
        communicator.get_patient_id()

    assert mock_input.call_count == 2


@patch('builtins.input', side_effect=['да', 'Да'])
def test_will_patient_discharge(mock_input):
    communicator = Communicator()

    assert communicator.will_patient_discharge()
    assert communicator.will_patient_discharge()
    assert mock_input.call_count == 2


@patch('sys.stdout', new_callable=StringIO)
def test_will_patient_discharge_prompt(mock_prompt):
    communicator = Communicator()

    with patch('sys.stdin', StringIO('да')):
        communicator.will_patient_discharge()

    assert mock_prompt.getvalue() == 'Желаете этого клиента выписать? (да/нет): '


@patch('builtins.input', side_effect=['нет', 'не нужно', 'yes', 'выпиши конечно'])
def test_will_patient_discharge_when_answer_is_not_yes(mock_input):
    communicator = Communicator()

    assert communicator.will_patient_discharge() is False
    assert communicator.will_patient_discharge() is False
    assert communicator.will_patient_discharge() is False
    assert communicator.will_patient_discharge() is False
    assert mock_input.call_count == 4


@pytest.mark.parametrize("user_answer", ['да', 'не нужно', 'yes', 'выпиши конечно'])
def test_will_patient_discharge_when_answer_is_not_yes_with_parametrize(user_answer):
    communicator = Communicator()

    with patch('builtins.input', return_value=user_answer):
        assert communicator.will_patient_discharge() is False
