from hospital import Hospital
from communicator import Communicator


class CommandHandler:
    """
    Обработчик команд
    """

    def __init__(self):
        self._hospital = Hospital()
        self._communicator = Communicator()

    def get_status(self):
        """
        Сценарий получения статуса пациента
        """

        try:
            patient_id = self._communicator.get_patient_id()
            patient_status = self._hospital.get_status(patient_id)
            self._communicator.send_message(f'Статус пациента: "{patient_status}"')
        except (ValueError, TypeError):
            self._communicator.send_message("Ошибка. ID пациента должно быть числом (целым, положительным)")
        except IndexError:
            self._communicator.send_message("Ошибка. В больнице нет пациента с таким ID.")

    def status_up(self):
        """
        Сценарий повышения статуса пациента
        """

        try:
            patient_id = self._communicator.get_patient_id()
            patient_current_status = self._hospital.get_status(patient_id)
            if patient_current_status == 'Готов к выписке':
                can_discharge = self._communicator.is_answer_yes('Желаете этого клиента выписать?')
                if can_discharge:
                    self._hospital.discharge(patient_id)
                    self._communicator.send_message('Пациент выписан из больницы')
                else:
                    self._communicator.send_message(f'Пациент остался в статусе "{patient_current_status}"')
            else:
                self._hospital.status_up(patient_id)
                new_patient_status = self._hospital.get_status(patient_id)
                self._communicator.send_message(f'Новый статус пациента: "{new_patient_status}"')
        except (ValueError, TypeError):
            self._communicator.send_message("Ошибка. ID пациента должно быть числом (целым, положительным)")
        except IndexError:
            self._communicator.send_message("Ошибка. В больнице нет пациента с таким ID.")

    def status_down(self):
        """
        Сценарий понижения статуса пациента
        """

        try:
            patient_id = self._communicator.get_patient_id()
            patient_current_status = self._hospital.get_status(patient_id)
            if patient_current_status == 'Тяжело болен':
                self._communicator.send_message('Ошибка. Нельзя понизить самый низкий статус (наши пациенты не '
                                                'умирают)')
            else:
                self._hospital.status_down(patient_id)
                new_patient_status = self._hospital.get_status(patient_id)
                self._communicator.send_message(f'Новый статус пациента: "{new_patient_status}"')
        except (ValueError, TypeError):
            self._communicator.send_message("Ошибка. ID пациента должно быть числом (целым, положительным)")
        except IndexError:
            self._communicator.send_message("Ошибка. В больнице нет пациента с таким ID.")

    def discharge(self):
        """
        Сценарий выписки пациента
        """

        try:
            patient_id = self._communicator.get_patient_id()
            self._hospital.discharge(patient_id)
            self._communicator.send_message('Пациент выписан из больницы')
        except (ValueError, TypeError):
            self._communicator.send_message("Ошибка. ID пациента должно быть числом (целым, положительным)")
        except IndexError:
            self._communicator.send_message("Ошибка. В больнице нет пациента с таким ID.")

    def calculate_statistics(self):
        """
        Сценарий расчета статистики
        """

        statistics = self._hospital.get_statistics()
        self._communicator.send_message(f"В больнице на данный момент находится {statistics['total']} чел., из них:")
        if statistics['hard_ill'] > 0:
            self._communicator.send_message(f"\t- в статусе \"Тяжело болен\": {statistics['hard_ill']} чел.")
        if statistics['normal_ill'] > 0:
            self._communicator.send_message(f"\t- в статусе \"Болен\": {statistics['normal_ill']} чел.")
        if statistics['easy_ill'] > 0:
            self._communicator.send_message(f"\t- в статусе \"Слегка болен\": {statistics['easy_ill']} чел.")
        if statistics['ready_for_discharge'] > 0:
            self._communicator.send_message(f"\t- в статусе \"Готов для выписки\": {statistics['ready_for_discharge']}"
                                             f" чел.")
