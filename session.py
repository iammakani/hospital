from base import Base
from patient import Patient


class Session:
    """
    Класс, описывающий сессию взаимодействия с пользователем
    """

    def __init__(self):
        self.enabled = True
        self.base = Base()
        self.patient = Patient(self.base.statuses, self.base.patients)

    def start(self):
        """
        Запуск программы - основной цикл программы
        """

        while self.enabled:
            self.read_command(input("Введите команду: "))

    def read_command(self, command):
        """
        Принимаем команду от пользователя, выполняем соответствующие действия
        """

        formatted_cmd = command.lower()

        match formatted_cmd:
            case "узнать статус пациента" | "get status":
                patient_id = self.read_patient_id()
                if patient_id:
                    self.patient.get_status(patient_id)

            case "повысить статус пациента" | "status up":
                patient_id = self.read_patient_id()
                if patient_id:
                    self.patient.status_up(patient_id)

            case "понизить статус пациента" | "status down":
                patient_id = self.read_patient_id()
                if patient_id:
                    self.patient.status_down(patient_id)

            case "выписать пациента" | "discharge":
                patient_id = self.read_patient_id()
                if patient_id:
                    self.patient.discharge(patient_id)

            case "рассчитать статистику" | "calculate statistics":
                self.base.calculate_statistics()

            case "стоп" | "stop":
                print("Сеанс завершён.")
                self.enabled = False

            case _:
                print("Неизвестная команда! Попробуйте ещё раз")

    def read_patient_id(self):
        """
        Читаеем ID и проверяем на валидность ID и наличие пациента с таким ID в базе
        ID для работы со списком передается как есть (понижается непосредственно в методах класса Patient)
        """

        patient_id = input("Введите ID пациента: ")
        if self.check_is_valid_patient_id(patient_id):
            if self.base.check_is_patient_in_patients(patient_id):
                return int(patient_id)

    def check_is_valid_patient_id(self, patient_id):
        """
        Проверка: ID пациента должно быть целове положительное число
        """

        try:
            if int(patient_id) > 0:
                return True
            else:
                print("Ошибка. ID пациента должно быть числом (целым, положительным)")
        except ValueError:
            print("Ошибка. ID пациента должно быть числом (целым, положительным)")
        return False
