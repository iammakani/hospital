class Hospital:
    """
    Класс, определяющий действия для работы с пациентами (без привязки к конкретному пациенту)
    """

    def __init__(self):
        self.__patients = [1 for _ in range(0, 200)]
        self.__statuses = {0: "Тяжело болен",
                           1: "Болен",
                           2: "Слегка болен",
                           3: "Готов к выписке"}

    def status_up(self, patient_id):
        """
        Повысить статус пациента
        """

        try:
            status_digital = self.__patients[patient_id - 1]
            if status_digital < 3:
                self.__patients[patient_id - 1] += 1
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
            status_digital = self.__patients[patient_id - 1]
            if status_digital > 0:
                self.__patients[patient_id - 1] -= 1
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
            if not self.__patients[patient_id - 1]:
                return False
            else:
                self.__patients[patient_id - 1] = None
                return True
        except Exception as error:
            print(f'Логируем ошибку: {error}')

    def get_status(self, patient_id):
        """
        Получаем статус пациента в цифровом виде
        """

        try:
            if int(patient_id) - 1 < len(self.__patients) and self.__patients[int(patient_id) - 1] is not None:
                status_digital = int(self.__patients[patient_id - 1])
                status = self.__statuses[status_digital]
                return status
        except Exception as error:
            print(f'Логируем ошибку: {error}')

    def calculate_statistics(self):
        """
        Расчет и вывод статистики
        """

        statistics = {'total': len(self.__patients) - self.__patients.count(None),
                      'hard_ill': self.__patients.count(0),
                      'normal_ill': self.__patients.count(1),
                      'easy_ill': self.__patients.count(2),
                      'ready_for_discharge': self.__patients.count(3)}

        return statistics

    def check_is_patient_in_patients(self, patient_id):
        """
        Проверка: пациент с введенным ID существует в базе
        """

        try:
            if int(patient_id) - 1 < len(self.__patients) and self.__patients[int(patient_id) - 1] is not None:
                return True
            return False
        except Exception as error:
            print(f'Логируем ошибку: {error}')
