class Patient:
    """
    Класс, определяющий действия для работы с пациентами (без привязки к конкретному пациенту)
    """

    def __init__(self, statuses, patients):
        self.patients = patients
        self.statuses = statuses

    def get_status(self, patient_id):
        """
        Вывести текущий статус пациента
        """

        status_digital = self.patients[patient_id-1]
        status_human_readable = self.statuses[status_digital]
        print(f'Статус пациента: "{status_human_readable}"')

    def status_up(self, patient_id):
        """
        Повысить статус пациента
        Если статус равен "Готов к выписке", то предложить выписать пациента
        Если получен отказ на предложение выписать пациента - оставить статус без изменений
        """

        status_digital = self.patients[patient_id-1]
        if status_digital < 3:
            self.patients[patient_id-1] += 1
            new_status_digital = self.patients[patient_id-1]
            new_status_human_readable = self.statuses[new_status_digital]
            print(f'Новый статус пациента: "{new_status_human_readable}"')
        else:
            will_discharge = input("Желаете этого клиента выписать? (да/нет): ")
            if will_discharge.lower() == "да":
                self.discharge(patient_id)
            else:
                status_digital = self.patients[patient_id-1]
                status_human_readable = self.statuses[status_digital]
                print(f'Пациент остался в статусе "{status_human_readable}"')

    def status_down(self, patient_id):
        """
        Понизить статус пациента
        Если статус равен "Тяжело болен" - оставить статус без изменений (просто вывести сообщение)
        """

        status_digital = self.patients[patient_id-1]
        if status_digital > 0:
            self.patients[patient_id-1] -= 1
            new_status_digital = self.patients[patient_id - 1]
            new_status_human_readable = self.statuses[new_status_digital]
            print(f'Новый статус пациента: "{new_status_human_readable}"')
        else:
            print('Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)')

    def discharge(self, patient_id):
        """
        Пациент удаляется из базы
        ID удаленного пациента в базе становится равно None
        """

        self.patients[patient_id-1] = None
        print('Пациент выписан из больницы')
