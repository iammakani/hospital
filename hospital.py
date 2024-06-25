from errors import PatientNotExists, PatientMaxStatusError, PatientMinStatusError


class Hospital:
    """
    Сущность, определяющие критические бизнесс правила
    """
    def __init__(self, patients):
        self._patients = patients
        self._statuses = {0: "Тяжело болен",
                          1: "Болен",
                          2: "Слегка болен",
                          3: "Готов к выписке"}

    def status_up(self, patient_id: int):
        self._verify_patient_exists(patient_id)
        status_digital = self._patients[patient_id - 1]
        if status_digital < 3:
            self._patients[patient_id - 1] += 1
        else:
            raise PatientMaxStatusError

    def status_down(self, patient_id: int):
        self._verify_patient_exists(patient_id)
        status_digital = self._patients[patient_id - 1]
        if status_digital > 0:
            self._patients[patient_id - 1] -= 1
        else:
            raise PatientMinStatusError

    def discharge(self, patient_id: int):
        """
        Пациент удаляется из базы - фактически ID удаленного пациента в базе становится равно None
        """
        self._verify_patient_exists(patient_id)
        self._patients[patient_id - 1] = None

    def get_status(self, patient_id: int):
        self._verify_patient_exists(patient_id)
        status_digital = int(self._patients[patient_id - 1])
        status = self._statuses[status_digital]
        return status

    def get_statistics(self):
        statistics = {'total': len(self._patients) - self._patients.count(None),
                      'hard_ill': self._patients.count(0),
                      'normal_ill': self._patients.count(1),
                      'easy_ill': self._patients.count(2),
                      'ready_for_discharge': self._patients.count(3)}

        return statistics

    def _verify_patient_exists(self, patient_id: int):
        if not (int(patient_id) - 1 < len(self._patients) and self._patients[int(patient_id) - 1] is not None):
            raise PatientNotExists

    def can_status_up(self, patient_id: int):
        self._verify_patient_exists(patient_id)
        status_digital = self._patients[patient_id - 1]
        return status_digital < 3

    def can_status_down(self, patient_id: int):
        self._verify_patient_exists(patient_id)
        status_digital = self._patients[patient_id - 1]
        return status_digital > 0
