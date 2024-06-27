from hospital import Hospital
from communicator import Communicator
from errors import IdValueError, PatientNotExists


class CommandHandler:
    _default_hospital = Hospital([1 for _ in range(0, 200)])
    _default_communicator = Communicator()

    def __init__(self, hospital=_default_hospital, communicator=_default_communicator):
        self._hospital = hospital
        self._communicator = communicator

    def get_status(self):
        try:
            patient_id = self._communicator.get_patient_id()
            patient_status = self._hospital.get_status(patient_id)
            self._communicator.send_message(f'Статус пациента: "{patient_status}"')
        except (IdValueError, PatientNotExists) as error:
            self._communicator.send_message(str(error))

    def status_up(self):
        try:
            patient_id = self._communicator.get_patient_id()
            if self._hospital.can_status_up(patient_id):
                self._hospital.status_up(patient_id)
                new_patient_status = self._hospital.get_status(patient_id)
                self._communicator.send_message(f'Новый статус пациента: "{new_patient_status}"')
            else:
                if self._communicator.will_patient_discharge():
                    self._hospital.discharge(patient_id)
                    self._communicator.send_message('Пациент выписан из больницы')
                else:
                    patient_current_status = self._hospital.get_status(patient_id)
                    self._communicator.send_message(f'Пациент остался в статусе "{patient_current_status}"')
        except (IdValueError, PatientNotExists) as error:
            self._communicator.send_message(str(error))

    def status_down(self):
        try:
            patient_id = self._communicator.get_patient_id()
            if self._hospital.can_status_down(patient_id):
                self._hospital.status_down(patient_id)
                new_patient_status = self._hospital.get_status(patient_id)
                self._communicator.send_message(f'Новый статус пациента: "{new_patient_status}"')
            else:
                self._communicator.send_message('Ошибка. Нельзя понизить самый низкий статус (наши пациенты не '
                                                'умирают)')
        except (IdValueError, PatientNotExists) as error:
            self._communicator.send_message(str(error))

    def discharge(self):
        try:
            patient_id = self._communicator.get_patient_id()
            self._hospital.discharge(patient_id)
            self._communicator.send_message('Пациент выписан из больницы')
        except (IdValueError, PatientNotExists) as error:
            self._communicator.send_message(str(error))

    def get_statistics(self):
        statistics = self._hospital.get_statistics()
        result = f"В больнице на данный момент находится {statistics['total']} чел., из них:"
        if statistics['hard_ill'] > 0:
            result += f"\n\t- в статусе \"Тяжело болен\": {statistics['hard_ill']} чел."
        if statistics['normal_ill'] > 0:
            result += f"\n\t- в статусе \"Болен\": {statistics['normal_ill']} чел."
        if statistics['easy_ill'] > 0:
            result += f"\n\t- в статусе \"Слегка болен\": {statistics['easy_ill']} чел."
        if statistics['ready_for_discharge'] > 0:
            result += f"\n\t- в статусе \"Готов для выписки\": {statistics['ready_for_discharge']} чел."
        self._communicator.send_message(result)
