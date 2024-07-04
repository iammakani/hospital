from session import Session

from unittest.mock import patch, call


@patch('builtins.print')
@patch('builtins.input', side_effect=['узнать статус пациента',
                                      '200',
                                      'status up',
                                      '2',
                                      'status down',
                                      '3',
                                      'discharge',
                                      '4',
                                      'рассчитать статистику',
                                      'стоп'])
def test_application_work_when_basic_scenario(_, mock_print):
    session = Session()

    session.start()

    mock_print.assert_has_calls([call('Статус пациента: "Болен"'),
                                 call('Новый статус пациента: "Слегка болен"'),
                                 call('Новый статус пациента: "Тяжело болен"'),
                                 call('Пациент выписан из больницы'),
                                 call(f'В больнице на данный момент находится 199 чел., из них:\n'
                                      f'\t- в статусе "Тяжело болен": 1 чел.\n'
                                      f'\t- в статусе "Болен": 197 чел.\n'
                                      f'\t- в статусе "Слегка болен": 1 чел.'),
                                 call('Сеанс завершён.')])


@patch('builtins.print')
@patch('builtins.input', side_effect=['выписать всех пациентов',
                                      'стоп'])
def test_application_work_when_unknown_command(_, mock_print):
    session = Session()

    session.start()

    mock_print.assert_has_calls([call('Неизвестная команда! Попробуйте ещё раз'),
                                 call('Сеанс завершён.')])


@patch('builtins.print')
@patch('builtins.input', side_effect=['узнать статус пациента',
                                      '7',
                                      'GET STATUS',
                                      '7',
                                      'Узнать СТАТУС пациентА',
                                      '7',
                                      'стоп'])
def test_application_work_when_different_types_of_input(_, mock_print):
    session = Session()

    session.start()

    mock_print.assert_has_calls([call('Статус пациента: "Болен"'),
                                 call('Статус пациента: "Болен"'),
                                 call('Статус пациента: "Болен"'),
                                 call('Сеанс завершён.')])


@patch('builtins.print')
@patch('builtins.input', side_effect=['узнать статус пациента',
                                      'два',
                                      'повысить статус пациента',
                                      '-2',
                                      'понизить статус пациента',
                                      '201',
                                      'стоп'])
def test_application_work_when_invalid_input(_, mock_print):
    session = Session()

    session.start()

    mock_print.assert_has_calls([call('Ошибка. ID пациента должно быть числом (целым, положительным)'),
                                 call('Ошибка. ID пациента должно быть числом (целым, положительным)'),
                                 call('Ошибка. В больнице нет пациента с таким ID.'),
                                 call('Сеанс завершён.')])


@patch('builtins.print')
@patch('builtins.input', side_effect=['повысить статус пациента',
                                      '1',
                                      'повысить статус пациента',
                                      '1',
                                      'повысить статус пациента',
                                      '1',
                                      'да',
                                      'рассчитать статистику',
                                      'стоп'])
def test_application_work_when_status_up_and_patient_discharged(_, mock_print):
    session = Session()

    session.start()

    mock_print.assert_has_calls([call('Новый статус пациента: "Слегка болен"'),
                                 call('Новый статус пациента: "Готов к выписке"'),
                                 call('Пациент выписан из больницы'),
                                 call(f'В больнице на данный момент находится 199 чел., из них:\n'
                                      f'\t- в статусе "Болен": 199 чел.'),
                                 call('Сеанс завершён.')])


@patch('builtins.print')
@patch('builtins.input', side_effect=['повысить статус пациента',
                                      '1',
                                      'повысить статус пациента',
                                      '1',
                                      'повысить статус пациента',
                                      '1',
                                      'нет',
                                      'рассчитать статистику',
                                      'стоп'])
def test_application_work_when_status_up_and_patient_not_discharged(_, mock_print):
    session = Session()

    session.start()

    mock_print.assert_has_calls([call('Новый статус пациента: "Слегка болен"'),
                                 call('Новый статус пациента: "Готов к выписке"'),
                                 call('Пациент остался в статусе "Готов к выписке"'),
                                 call(f'В больнице на данный момент находится 200 чел., из них:\n'
                                      f'\t- в статусе "Болен": 199 чел.\n'
                                      f'\t- в статусе "Готов к выписке": 1 чел.'),
                                 call('Сеанс завершён.')])


@patch('builtins.print')
@patch('builtins.input', side_effect=['понизить статус пациента',
                                      '1',
                                      'понизить статус пациента',
                                      '1',
                                      'рассчитать статистику',
                                      'стоп'])
def test_application_work_when_status_down_while_status_already_min(_, mock_print):
    session = Session()

    session.start()

    mock_print.assert_has_calls([call('Новый статус пациента: "Тяжело болен"'),
                                 call('Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)'),
                                 call(f'В больнице на данный момент находится 200 чел., из них:\n'
                                      f'\t- в статусе "Тяжело болен": 1 чел.\n'
                                      f'\t- в статусе "Болен": 199 чел.'),
                                 call('Сеанс завершён.')])
