from command_handler import CommandHandler
from errors import IdValueError
from hospital import Hospital
from unittest.mock import MagicMock


def test_get_status():
    command_handler = CommandHandler(Hospital([0, 1]), MagicMock())
    command_handler._communicator.get_patient_id = MagicMock(return_value=2)

    command_handler.get_status()

    command_handler._communicator.send_message.assert_called_with('Статус пациента: "Болен"')


def test_get_status_when_patient_not_exists():
    command_handler = CommandHandler(Hospital([0, 1]), MagicMock())
    command_handler._communicator.get_patient_id = MagicMock(return_value=3)

    command_handler.get_status()

    command_handler._communicator.send_message.assert_called_with('Ошибка. В больнице нет пациента с таким ID.')


def test_get_status_when_patient_is_already_discharged():
    command_handler = CommandHandler(Hospital([0, None, 1]), MagicMock())
    command_handler._communicator.get_patient_id = MagicMock(return_value=2)

    command_handler.get_status()

    command_handler._communicator.send_message.assert_called_with('Ошибка. В больнице нет пациента с таким ID.')


def test_get_status_when_patient_is_not_valid():
    command_handler = CommandHandler(Hospital([0, 1]), MagicMock())
    command_handler._hospital.get_status = MagicMock(side_effect=IdValueError)

    command_handler.get_status()

    command_handler._communicator.send_message.assert_called_with('Ошибка. ID пациента должно быть числом (целым, '
                                                                  'положительным)')


def test_status_up():
    command_handler = CommandHandler(Hospital([0, 1]), MagicMock())
    command_handler._communicator.get_patient_id = MagicMock(return_value=2)

    command_handler.status_up()

    assert command_handler._hospital._patients == [0, 2]
    command_handler._communicator.send_message.assert_called_with('Новый статус пациента: "Слегка болен"')


def test_status_up_when_patient_id_not_valid():
    command_handler = CommandHandler(Hospital([0, 1]), MagicMock())
    command_handler._communicator.get_patient_id = MagicMock(side_effect=IdValueError)

    command_handler.status_up()

    assert command_handler._hospital._patients == [0, 1]
    command_handler._communicator.send_message.assert_called_with('Ошибка. ID пациента должно быть числом (целым, '
                                                                  'положительным)')


def test_status_up_when_patient_not_exists():
    command_handler = CommandHandler(Hospital([0, 1]), MagicMock())
    command_handler._communicator.get_patient_id = MagicMock(return_value=3)

    command_handler.status_up()

    assert command_handler._hospital._patients == [0, 1]
    command_handler._communicator.send_message.assert_called_with('Ошибка. В больнице нет пациента с таким ID.')


def test_status_up_when_patient_already_discharged():
    command_handler = CommandHandler(Hospital([0, None, 1]), MagicMock())
    command_handler._communicator.get_patient_id = MagicMock(return_value=2)

    command_handler.status_up()

    assert command_handler._hospital._patients == [0, None, 1]
    command_handler._communicator.send_message.assert_called_with('Ошибка. В больнице нет пациента с таким ID.')


def test_status_up_when_patient_has_max_status_and_will_discharge():
    command_handler = CommandHandler(Hospital([2, 3]), MagicMock())
    command_handler._communicator.get_patient_id = MagicMock(return_value=2)
    command_handler._communicator.will_patient_discharge = MagicMock(return_value=True)

    command_handler.status_up()

    assert command_handler._hospital._patients == [2, None]
    command_handler._communicator.send_message.assert_called_with('Пациент выписан из больницы')


def test_status_up_when_patient_has_max_status_and_will_not_discharge():
    command_handler = CommandHandler(Hospital([2, 3]), MagicMock())
    command_handler._communicator.get_patient_id = MagicMock(return_value=2)
    command_handler._communicator.will_patient_discharge = MagicMock(return_value=False)

    command_handler.status_up()

    assert command_handler._hospital._patients == [2, 3]
    command_handler._communicator.send_message.assert_called_with('Пациент остался в статусе "Готов к выписке"')


def test_status_down():
    command_handler = CommandHandler(Hospital([1, 3]), MagicMock())
    command_handler._communicator.get_patient_id = MagicMock(return_value=2)

    command_handler.status_down()

    assert command_handler._hospital._patients == [1, 2]
    command_handler._communicator.send_message.assert_called_with('Новый статус пациента: "Слегка болен"')


def test_status_down_when_patient_id_not_valid():
    command_handler = CommandHandler(Hospital([0, 1]), MagicMock())
    command_handler._communicator.get_patient_id = MagicMock(side_effect=IdValueError)

    command_handler.status_down()

    assert command_handler._hospital._patients == [0, 1]
    command_handler._communicator.send_message.assert_called_with('Ошибка. ID пациента должно быть числом (целым, '
                                                                  'положительным)')


def test_status_down_when_patient_not_exists():
    command_handler = CommandHandler(Hospital([0, 1]), MagicMock())
    command_handler._communicator.get_patient_id = MagicMock(return_value=3)

    command_handler.status_down()

    assert command_handler._hospital._patients == [0, 1]
    command_handler._communicator.send_message.assert_called_with('Ошибка. В больнице нет пациента с таким ID.')


def test_status_down_when_patient_already_discharged():
    command_handler = CommandHandler(Hospital([0, None, 1]), MagicMock())
    command_handler._communicator.get_patient_id = MagicMock(return_value=2)

    command_handler.status_down()

    assert command_handler._hospital._patients == [0, None, 1]
    command_handler._communicator.send_message.assert_called_with('Ошибка. В больнице нет пациента с таким ID.')


def test_status_down_when_patient_has_min_status():
    command_handler = CommandHandler(Hospital([0, 2]), MagicMock())
    command_handler._communicator.get_patient_id = MagicMock(return_value=1)

    command_handler.status_down()

    assert command_handler._hospital._patients == [0, 2]
    command_handler._communicator.send_message.assert_called_with('Ошибка. Нельзя понизить самый низкий статус (наши '
                                                                  'пациенты не умирают)')


def test_discharge():
    command_handler = CommandHandler(Hospital([1, 3]), MagicMock())
    command_handler._communicator.get_patient_id = MagicMock(return_value=2)

    command_handler.discharge()

    assert command_handler._hospital._patients == [1, None]
    command_handler._communicator.send_message.assert_called_with('Пациент выписан из больницы')


def test_discharge_when_patient_id_not_valid():
    command_handler = CommandHandler(Hospital([0, 1]), MagicMock())
    command_handler._communicator.get_patient_id = MagicMock(side_effect=IdValueError)

    command_handler.discharge()

    assert command_handler._hospital._patients == [0, 1]
    command_handler._communicator.send_message.assert_called_with('Ошибка. ID пациента должно быть числом (целым, '
                                                                  'положительным)')


def test_discharge_when_patient_not_exists():
    command_handler = CommandHandler(Hospital([1, 2]), MagicMock())
    command_handler._communicator.get_patient_id = MagicMock(return_value=3)

    command_handler.discharge()

    assert command_handler._hospital._patients == [1, 2]
    command_handler._communicator.send_message.assert_called_with('Ошибка. В больнице нет пациента с таким ID.')


def test_discharge_when_patient_already_discharged():
    command_handler = CommandHandler(Hospital([1, None, 3]), MagicMock())
    command_handler._communicator.get_patient_id = MagicMock(return_value=2)

    command_handler.discharge()

    assert command_handler._hospital._patients == [1, None, 3]
    command_handler._communicator.send_message.assert_called_with('Ошибка. В больнице нет пациента с таким ID.')


def test_get_statistics():
    command_handler = CommandHandler(Hospital([1, 0, None, 1, 3, 0, None, 1]), MagicMock())

    command_handler.get_statistics()

    expected_statistics = f'В больнице на данный момент находится 6 чел., из них:' \
                          f'\n\t- в статусе "Тяжело болен": 2 чел.' \
                          f'\n\t- в статусе "Болен": 3 чел.' \
                          f'\n\t- в статусе "Готов для выписки": 1 чел.'
    command_handler._communicator.send_message.assert_called_with(expected_statistics)
