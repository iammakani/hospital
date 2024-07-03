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


# Нормально ли делать так как ниже?
# На мой взгляд, тест содержит одну логику - проверку негативных сценариев
# Визуально, он так же довольно органичен, видно что идет проверка появления конкретного исключения при подставлении
#       значений из списка
# Или всё же правильнее разбивать на более мелкие тесты?
@patch('builtins.input', side_effect=['-2', '0', 'Q', 'Test', 'Я', 'Тест'])
def test_get_patient_id_when_value_is_not_valid(mock_input):
    communicator = Communicator()

    with pytest.raises(IdValueError):
        communicator.get_patient_id()

    with pytest.raises(IdValueError):
        communicator.get_patient_id()

    with pytest.raises(IdValueError):
        communicator.get_patient_id()

    with pytest.raises(IdValueError):
        communicator.get_patient_id()

    with pytest.raises(IdValueError):
        communicator.get_patient_id()

    with pytest.raises(IdValueError):
        communicator.get_patient_id()

    assert mock_input.call_count == 6


@patch('sys.stdout', new_callable=StringIO)
def test_will_patient_discharge_prompt(mock_prompt):
    communicator = Communicator()
    with patch('sys.stdin', StringIO('да')):

        communicator.will_patient_discharge()

    assert mock_prompt.getvalue() == 'Желаете этого клиента выписать? (да/нет): '


@patch('builtins.input', side_effect=['да', 'Да', 'ДА'])
def test_will_patient_discharge(mock_input):
    communicator = Communicator()

    assert communicator.will_patient_discharge() is True
    assert communicator.will_patient_discharge() is True
    assert communicator.will_patient_discharge() is True
    assert mock_input.call_count == 3


@patch('builtins.input', side_effect=['нет', 'no', 'yes', 'Qwe', '123'])
def test_will_patient_discharge_when_answer_is_not_yes(mock_input):
    communicator = Communicator()

    assert communicator.will_patient_discharge() is False
    assert communicator.will_patient_discharge() is False
    assert communicator.will_patient_discharge() is False
    assert communicator.will_patient_discharge() is False
    assert communicator.will_patient_discharge() is False
    assert mock_input.call_count == 5
