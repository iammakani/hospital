from command_handler import CommandHandler
from errors import IdValueError
from hospital import Hospital
from unittest.mock import MagicMock


# Тут вопрос для обсуждения:
#
# С учетом того, что мы обусловились не проверять факт передачи именно числового значения в бизнесс логику - на этом
# этапе не могу выполнить тест при передаче данных типа str в command_handler.get_status()
#
# На сколько я понял, MagicMock напрямую возвращает значение по запросу command_handler._communicator.get_patient_id(),
# а проверка осуществляется как раз в работе самого метода
#
# Остается только вариант, когда у нас метод command_handler._communicator.get_patient_id() возвращает ошибку - т.е.
# мы его заранее мокаем на ошибку IdValueError


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
    command_handler._communicator.send_message.assert_called_with('Новый статус пациента: "Слегка болен"')
    assert command_handler._hospital._patients == [0, 2]


def test_status_up_when_patient_id_not_valid():
    command_handler = CommandHandler(Hospital([0, 1]), MagicMock())
    command_handler._communicator.get_patient_id = MagicMock(side_effect=IdValueError)
    command_handler.status_up()
    command_handler._communicator.send_message.assert_called_with('Ошибка. ID пациента должно быть числом (целым, '
                                                                  'положительным)')
    assert command_handler._hospital._patients == [0, 1]


def test_status_up_when_patient_not_exists():
    command_handler = CommandHandler(Hospital([0, 1]), MagicMock())
    command_handler._communicator.get_patient_id = MagicMock(return_value=3)
    command_handler.status_up()
    command_handler._communicator.send_message.assert_called_with('Ошибка. В больнице нет пациента с таким ID.')
    assert command_handler._hospital._patients == [0, 1]


def test_status_up_when_patient_already_discharged():
    command_handler = CommandHandler(Hospital([0, None, 1]), MagicMock())
    command_handler._communicator.get_patient_id = MagicMock(return_value=2)
    command_handler.status_up()
    command_handler._communicator.send_message.assert_called_with('Ошибка. В больнице нет пациента с таким ID.')
    assert command_handler._hospital._patients == [0, None, 1]


def test_status_up_when_patient_has_max_status_and_will_discharge():
    command_handler = CommandHandler(Hospital([2, 3]), MagicMock())
    command_handler._communicator.get_patient_id = MagicMock(return_value=2)
    command_handler._communicator.will_patient_discharge = MagicMock(return_value=True)
    command_handler.status_up()
    command_handler._communicator.send_message.assert_called_with('Пациент выписан из больницы')
    assert command_handler._hospital._patients == [2, None]


def test_status_up_when_patient_has_max_status_and_will_not_discharge():
    command_handler = CommandHandler(Hospital([2, 3]), MagicMock())
    command_handler._communicator.get_patient_id = MagicMock(return_value=2)
    command_handler._communicator.will_patient_discharge = MagicMock(return_value=False)
    command_handler.status_up()
    command_handler._communicator.send_message.assert_called_with('Пациент остался в статусе "Готов к выписке"')
    assert command_handler._hospital._patients == [2, 3]


def test_status_down():
    command_handler = CommandHandler(Hospital([1, 3]), MagicMock())
    command_handler._communicator.get_patient_id = MagicMock(return_value=2)
    command_handler.status_down()
    command_handler._communicator.send_message.assert_called_with('Новый статус пациента: "Слегка болен"')
    assert command_handler._hospital._patients == [1, 2]


def test_status_down_when_patient_id_not_valid():
    command_handler = CommandHandler(Hospital([0, 1]), MagicMock())
    command_handler._communicator.get_patient_id = MagicMock(side_effect=IdValueError)
    command_handler.status_down()
    command_handler._communicator.send_message.assert_called_with('Ошибка. ID пациента должно быть числом (целым, '
                                                                  'положительным)')
    assert command_handler._hospital._patients == [0, 1]


def test_status_down_when_patient_not_exists():
    command_handler = CommandHandler(Hospital([0, 1]), MagicMock())
    command_handler._communicator.get_patient_id = MagicMock(return_value=3)
    command_handler.status_down()
    command_handler._communicator.send_message.assert_called_with('Ошибка. В больнице нет пациента с таким ID.')
    assert command_handler._hospital._patients == [0, 1]


def test_status_down_when_patient_already_discharged():
    command_handler = CommandHandler(Hospital([0, None, 1]), MagicMock())
    command_handler._communicator.get_patient_id = MagicMock(return_value=2)
    command_handler.status_down()
    command_handler._communicator.send_message.assert_called_with('Ошибка. В больнице нет пациента с таким ID.')
    assert command_handler._hospital._patients == [0, None, 1]


def test_status_down_when_patient_has_min_status():
    command_handler = CommandHandler(Hospital([0, 2]), MagicMock())
    command_handler._communicator.get_patient_id = MagicMock(return_value=1)
    command_handler.status_down()
    command_handler._communicator.send_message.assert_called_with('Ошибка. Нельзя понизить самый низкий статус (наши '
                                                                  'пациенты не умирают)')
    assert command_handler._hospital._patients == [0, 2]


def test_discharge():
    command_handler = CommandHandler(Hospital([1, 3]), MagicMock())
    command_handler._communicator.get_patient_id = MagicMock(return_value=2)
    command_handler.discharge()
    command_handler._communicator.send_message.assert_called_with('Пациент выписан из больницы')
    assert command_handler._hospital._patients == [1, None]


def test_discharge_when_patient_id_not_valid():
    command_handler = CommandHandler(Hospital([0, 1]), MagicMock())
    command_handler._communicator.get_patient_id = MagicMock(side_effect=IdValueError)
    command_handler.discharge()
    command_handler._communicator.send_message.assert_called_with('Ошибка. ID пациента должно быть числом (целым, '
                                                                  'положительным)')
    assert command_handler._hospital._patients == [0, 1]


def test_discharge_when_patient_not_exists():
    command_handler = CommandHandler(Hospital([1, 2]), MagicMock())
    command_handler._communicator.get_patient_id = MagicMock(return_value=3)
    command_handler.discharge()
    command_handler._communicator.send_message.assert_called_with('Ошибка. В больнице нет пациента с таким ID.')
    assert command_handler._hospital._patients == [1, 2]


def test_discharge_when_patient_already_discharged():
    command_handler = CommandHandler(Hospital([1, None, 3]), MagicMock())
    command_handler._communicator.get_patient_id = MagicMock(return_value=2)
    command_handler.discharge()
    command_handler._communicator.send_message.assert_called_with('Ошибка. В больнице нет пациента с таким ID.')
    assert command_handler._hospital._patients == [1, None, 3]


def test_get_statistics():
    command_handler = CommandHandler(Hospital([3, 1, None, 2, 3, 1, None, 3]), MagicMock())
    command_handler.get_statistics()
    expected_statistics = f'В больнице на данный момент находится 6 чел., из них:\n\t- в статусе "Болен": 2 чел.' \
                          f'\n\t- в статусе "Слегка болен": 1 чел.\n\t- в статусе "Готов для выписки": 3 чел.'
    command_handler._communicator.send_message.assert_called_with(expected_statistics)



