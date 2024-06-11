from hospital import Hospital
from communicator import Communicator


class CommandHandler:
    """
    Обработчик команд
    """

    def __init__(self):
        self.__hospital = Hospital()
        self.__communicator = Communicator()

    def get_status(self):
        """
        Сценарий получения статуса пациента
        """

        patient_id = self.__communicator.read_patient_id()
        if patient_id:
            if self.__hospital.check_is_patient_in_patients(patient_id):
                patient_status = self.__hospital.get_status(patient_id)
                self.__communicator.send_message(f'Статус пациента: "{patient_status}"')
            else:
                self.__communicator.send_message("Ошибка. В больнице нет пациента с таким ID")

    def status_up(self):
        """
        Сценарий повышения статуса пациента
        """

        patient_id = self.__communicator.read_patient_id()
        if patient_id:
            if self.__hospital.check_is_patient_in_patients(patient_id):
                patient_current_status = self.__hospital.get_status(patient_id)
                if patient_current_status == 'Готов к выписке':
                    will_discharge = self.__communicator.read_yes_or_no('Желаете этого клиента выписать?')
                    if will_discharge:
                        if self.__hospital.discharge(patient_id):
                            self.__communicator.send_message('Пациент выписан из больницы')
                    else:
                        self.__communicator.send_message(f'Пациент остался в статусе "{patient_current_status}"')
                else:
                    if self.__hospital.status_up(patient_id):
                        new_patient_status = self.__hospital.get_status(patient_id)
                        self.__communicator.send_message(f'Новый статус пациента: "{new_patient_status}"')
            else:
                self.__communicator.send_message("Ошибка. В больнице нет пациента с таким ID")

    def status_down(self):
        """
        Сценарий понижения статуса пациента
        """

        patient_id = self.__communicator.read_patient_id()
        if patient_id:
            if self.__hospital.check_is_patient_in_patients(patient_id):
                patient_current_status = self.__hospital.get_status(patient_id)
                if patient_current_status == 'Тяжело болен':
                    self.__communicator.send_message('Ошибка. Нельзя понизить самый низкий статус (наши пациенты не '
                                                     'умирают)')
                else:
                    if self.__hospital.status_down(patient_id):
                        new_patient_status = self.__hospital.get_status(patient_id)
                        self.__communicator.send_message(f'Новый статус пациента: "{new_patient_status}"')
            else:
                self.__communicator.send_message("Ошибка. В больнице нет пациента с таким ID")

    def discharge(self):
        """
        Сценарий выписки пациента
        """

        patient_id = self.__communicator.read_patient_id()
        if patient_id:
            if self.__hospital.check_is_patient_in_patients(patient_id):
                if self.__hospital.discharge(patient_id):
                    self.__communicator.send_message('Пациент выписан из больницы')
            else:
                self.__communicator.send_message("Ошибка. В больнице нет пациента с таким ID")

    def calculate_statistics(self):
        """
        Сценарий расчета статистики
        """

        statistics = self.__hospital.calculate_statistics()
        self.__communicator.send_message(f"В больнице на данный момент находится {statistics['total']} чел., из них:")
        if statistics['hard_ill'] > 0:
            self.__communicator.send_message(f"\t- в статусе \"Тяжело болен\": {statistics['hard_ill']} чел.")
        if statistics['normal_ill'] > 0:
            self.__communicator.send_message(f"\t- в статусе \"Болен\": {statistics['normal_ill']} чел.")
        if statistics['easy_ill'] > 0:
            self.__communicator.send_message(f"\t- в статусе \"Слегка болен\": {statistics['easy_ill']} чел.")
        if statistics['ready_for_discharge'] > 0:
            self.__communicator.send_message(f"\t- в статусе \"Готов для выписки\": {statistics['ready_for_discharge']}"
                                             f" чел.")
