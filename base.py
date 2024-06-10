class Base:
    """
    Класс, описывающий базу пациентов и методы для работы с ней
    """

    def __init__(self):
        self.patients = [1 for i in range(0, 200)]
        self.statuses = {0: "Тяжело болен",
                         1: "Болен",
                         2: "Слегка болен",
                         3: "Готов к выписке"}

    def check_is_patient_in_patients(self, patient_id):
        """
        Проверка: пациент с введенным ID существует в базе
        """

        try:
            if int(patient_id) - 1 < len(self.patients) and self.patients[int(patient_id) - 1] is not None:
                return True
            return False
        except Exception as error:
            print(f'Логируем ошибку: {error}')

    def get_status_digital(self, patient_id):
        """
        Получаем статус пациента в цифровом виде
        """

        try:
            if int(patient_id) - 1 < len(self.patients) and self.patients[int(patient_id) - 1] is not None:
                return int(self.patients[patient_id - 1])
        except Exception as error:
            print(f'Логируем ошибку: {error}')

    def get_status_human_readable(self, patient_id):
        """
        Получаем статус пациента в человекочитаемом виде
        """

        try:
            status_digital = self.get_status_digital(patient_id)
            status_human_readable = self.statuses[status_digital]
            return status_human_readable
        except Exception as error:
            print(f'Логируем ошибку: {error}')

    def calculate_statistics(self):
        """
        Расчет и вывод статистики
        """

        statistics = {'total': len(self.patients) - self.patients.count(None),
                      'hard_ill': self.patients.count(0),
                      'normal_ill': self.patients.count(1),
                      'easy_ill': self.patients.count(2),
                      'ready_for_discharge': self.patients.count(3)}

        return statistics
