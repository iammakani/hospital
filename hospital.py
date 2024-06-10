class Hospital:
    """
    Класс, определяющий действия для работы с пациентами (без привязки к конкретному пациенту)
    """

    def __init__(self, statuses, patients):
        self.patients = patients
        self.statuses = statuses

    def status_up(self, patient_id):
        """
        Повысить статус пациента
        """

        try:
            status_digital = self.patients[patient_id-1]
            if status_digital < 3:
                self.patients[patient_id-1] += 1
                return True
            else:
                return False
        except Exception as error:
            print(f'Логируем ошибку: {error}')

    def status_down(self, patient_id):
        """
        Понизить статус пациента
        """

        try:
            status_digital = self.patients[patient_id-1]
            if status_digital > 0:
                self.patients[patient_id-1] -= 1
                return True
            else:
                return False
        except Exception as error:
            print(f'Логируем ошибку: {error}')

    def discharge(self, patient_id):
        """
        Пациент удаляется из базы
        ID удаленного пациента в базе становится равно None
        """

        try:
            self.patients[patient_id-1] = None
            return True
        except Exception as error:
            print(f'Логируем ошибку: {error}')
