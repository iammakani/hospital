import pytest

from communicator import Communicator2
from errors import IdValueError

from unittest.mock import MagicMock


def test_get_command():
    communicator2 = Communicator2(console=MagicMock())
    communicator2._console.input = MagicMock(side_effect=['get status', 'STATUS UP', 'РасСЧитАТЬ СтатИСтиКУ'])

    assert communicator2.get_command() == 'get status'
    assert communicator2.get_command() == 'status up'
    assert communicator2.get_command() == 'рассчитать статистику'

    assert communicator2._console.input.call_count == 3


def test_get_command_prompt():
    communicator2 = Communicator2(console=MagicMock())
    communicator2._console.input = MagicMock(return_value='get status')

    communicator2.get_command()

    communicator2._console.input.assert_called_with('Введите команду: ')


def test_get_patient_id():
    communicator2 = Communicator2(console=MagicMock())
    communicator2._console.input = MagicMock(return_value='2')

    assert communicator2.get_patient_id() == 2


def test_get_patient_id_prompt():
    communicator2 = Communicator2(console=MagicMock())
    communicator2._console.input = MagicMock(return_value='2')

    communicator2.get_patient_id()

    communicator2._console.input.assert_called_with('Введите ID пациента: ')


def test_get_patient_id_when_value_is_not_valid():
    communicator2 = Communicator2(console=MagicMock())
    communicator2._console.input = MagicMock(side_effect=['-2', '0', 'Q', 'Test', 'Я', 'Тест'])

    with pytest.raises(IdValueError):
        communicator2.get_patient_id()

    with pytest.raises(IdValueError):
        communicator2.get_patient_id()

    with pytest.raises(IdValueError):
        communicator2.get_patient_id()

    with pytest.raises(IdValueError):
        communicator2.get_patient_id()

    with pytest.raises(IdValueError):
        communicator2.get_patient_id()

    with pytest.raises(IdValueError):
        communicator2.get_patient_id()

    assert communicator2._console.input.call_count == 6


def test_will_patient_discharge():
    communicator2 = Communicator2(console=MagicMock())
    communicator2._console.input = MagicMock(side_effect=['да', 'Да', 'ДА', 'дА'])

    assert communicator2.will_patient_discharge() is True
    assert communicator2.will_patient_discharge() is True
    assert communicator2.will_patient_discharge() is True
    assert communicator2.will_patient_discharge() is True

    assert communicator2._console.input.call_count == 4


def test_will_patient_discharge_prompt():
    communicator2 = Communicator2(console=MagicMock())
    communicator2._console.input = MagicMock(return_value='да')

    communicator2.will_patient_discharge()

    communicator2._console.input.assert_called_with('Желаете этого клиента выписать? (да/нет): ')


def test_will_patient_discharge_when_answer_is_not_yes():
    communicator2 = Communicator2(console=MagicMock())
    communicator2._console.input = MagicMock(side_effect=['нет', 'no', 'yes', 'Qwe', '123'])

    assert communicator2.will_patient_discharge() is not True
    assert communicator2.will_patient_discharge() is not True
    assert communicator2.will_patient_discharge() is not True
    assert communicator2.will_patient_discharge() is not True
    assert communicator2.will_patient_discharge() is not True

    assert communicator2._console.input.call_count == 5
