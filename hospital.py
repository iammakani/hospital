class Hospital:
    """
    Класс, определяющий действия для работы с пациентами (без привязки к конкретному пациенту)
    """

    def __init__(self):
        self._patients = [1 for _ in range(0, 200)]
        self._statuses = {0: "Тяжело болен",
                          1: "Болен",
                          2: "Слегка болен",
                          3: "Готов к выписке"}

    def status_up(self, patient_id):
        """
        Повысить статус пациента
        """

        if not type(patient_id) is int:
            raise TypeError(f'Ошибка. ID пациента должно быть числом (целым, положительным).')

        if self._is_patient_exist(patient_id):
            status_digital = self._patients[patient_id - 1]
            if status_digital < 3:
                self._patients[patient_id - 1] += 1
            else:
                raise ValueError("Ошибка. У пациента уже максимально возможный статус.")
        else:
            raise IndexError("Ошибка. В больнице нет пациента с таким ID.")

    def status_down(self, patient_id):
        """
        Понизить статус пациента
        """

        if not type(patient_id) is int:
            raise TypeError(f'Ошибка. ID пациента должно быть числом (целым, положительным).')

        if self._is_patient_exist(patient_id):
            status_digital = self._patients[patient_id - 1]
            if status_digital > 0:
                self._patients[patient_id - 1] -= 1
            else:
                raise ValueError("Ошибка. У пациента уже минимально возможный статус")
        else:
            raise IndexError("Ошибка. В больнице нет пациента с таким ID.")

    def discharge(self, patient_id):
        """
        Пациент удаляется из базы
        ID удаленного пациента в базе становится равно None
        """

        if not type(patient_id) is int:
            raise TypeError(f'Ошибка. ID пациента должно быть числом (целым, положительным).')

        if self._is_patient_exist(patient_id):
            self._patients[patient_id - 1] = None
        else:
            raise IndexError("Ошибка. В больнице нет пациента с таким ID.")

    def get_status(self, patient_id):
        """
        Получаем статус пациента в цифровом виде
        """

        if not type(patient_id) is int:
            raise TypeError("Ошибка. ID пациента должно быть числом (целым, положительным).")

        if self._is_patient_exist(patient_id):
            status_digital = int(self._patients[patient_id - 1])
            status = self._statuses[status_digital]
            return status
        else:
            raise IndexError("Ошибка. В больнице нет пациента с таким ID.")

    def get_statistics(self):
        """
        Расчет и вывод статистики
        """

        statistics = {'total': len(self._patients) - self._patients.count(None),
                      'hard_ill': self._patients.count(0),
                      'normal_ill': self._patients.count(1),
                      'easy_ill': self._patients.count(2),
                      'ready_for_discharge': self._patients.count(3)}

        return statistics

    def _is_patient_exist(self, patient_id):
        """
        Проверка: пациент с введенным ID существует в базе
        """

        if int(patient_id) - 1 < len(self._patients) and self._patients[int(patient_id) - 1] is not None:
            return True
        return False
