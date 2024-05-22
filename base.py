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

        if int(patient_id)-1 < len(self.patients) and self.patients[int(patient_id)-1] is not None:
            return True
        else:
            print("Ошибка. В больнице нет пациента с таким ID")
        return False

    def calculate_statistics(self):
        """
        Расчет и вывод статистики
        """

        total = len(self.patients) - self.patients.count(None)
        hard_ill = self.patients.count(0)
        normal_ill = self.patients.count(1)
        easy_ill = self.patients.count(2)
        ready_for_discharge = self.patients.count(3)

        print(f'В больнице на данный момент находится {total} чел., из них:')
        if hard_ill > 0:
            print(f'\t- в статусе "Тяжело болен": {hard_ill} чел.')
        if normal_ill > 0:
            print(f'\t- в статусе "Болен": {normal_ill} чел.')
        if easy_ill > 0:
            print(f'\t- в статусе "Слегка болен": {easy_ill} чел.')
        if ready_for_discharge > 0:
            print(f'\t- в статусе "Готов для выписки": {ready_for_discharge} чел.')
