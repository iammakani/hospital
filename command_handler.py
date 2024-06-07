from hospital import Hospital
from base import Base


class CommandHandler:
    """
    Обработчик команд
    """

    def __init__(self, session):
        self.base = Base()
        self.hospital = Hospital(self.base.statuses, self.base.patients)
        self.session = session

    def do_command(self, command):
        """
        Выполняем действия в зависимости от принятой команды
        """
        match command:
            case "узнать статус пациента" | "get status":
                patient_id = self.session.read_patient_id()
                if patient_id:
                    if self.base.check_is_patient_in_patients(patient_id):
                        patient_status = self.base.get_status_human_readable(patient_id)
                        self.session.write(f'Статус пациента: "{patient_status}"')

            case "повысить статус пациента" | "status up":
                patient_id = self.session.read_patient_id()
                if patient_id:
                    if self.base.check_is_patient_in_patients(patient_id):
                        if self.base.get_status_digital(patient_id) < 3:
                            self.hospital.status_up(patient_id)
                            new_status_human_readable = self.base.get_status_human_readable(patient_id)
                            self.session.write(f'Новый статус пациента: "{new_status_human_readable}"')
                        else:
                            if self.session.ask_for_discharge() == 'да':
                                if self.hospital.discharge(patient_id):
                                    self.session.write('Пациент выписан из больницы')
                            else:
                                status_human_readable = self.base.get_status_human_readable(patient_id)
                                self.session.write(f'Пациент остался в статусе "{status_human_readable}"')

            case "понизить статус пациента" | "status down":
                patient_id = self.session.read_patient_id()
                if patient_id:
                    if self.base.check_is_patient_in_patients(patient_id):
                        if self.base.get_status_digital(patient_id) > 0:
                            self.hospital.status_down(patient_id)
                            new_status_human_readable = self.base.get_status_human_readable(patient_id)
                            self.session.write(f'Новый статус пациента: "{new_status_human_readable}"')
                        else:
                            self.session.write('Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)')

            case "выписать пациента" | "discharge":
                patient_id = self.session.read_patient_id()
                if patient_id:
                    if self.base.check_is_patient_in_patients(patient_id):
                        if self.hospital.discharge(patient_id):
                            self.session.write('Пациент выписан из больницы')

            case "рассчитать статистику" | "calculate statistics":
                self.base.calculate_statistics()

            case "стоп" | "stop":
                self.session.stop()

            case _:
                self.session.write("Неизвестная команда! Попробуйте ещё раз")
                self.session.read_command()
