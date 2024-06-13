class Communicator:
    """
    Класс, содержащий методы для взаимодействия с пользователем через командную строку
    """

    def get_command(self):
        """
        Запросить команду пользователя
        """

        command = input("Введите команду: ")
        formatted_command = command.lower()
        return formatted_command

    def get_patient_id(self):
        """
        Запросить id пациента
        """

        patient_id = input("Введите ID пациента: ")
        if self._is_valid_patient_id(patient_id):
            return int(patient_id)
        else:
            raise ValueError("Ошибка. ID пациента должно быть числом (целым, положительным)")

    def is_answer_yes(self, message=''):
        """
        Запросить ответ на вопрос "да/нет"
        """

        answer = input(f"{message} (да/нет): ").lower()
        if answer == 'да':
            return True
        return False

    def send_message(self, message):
        """
        Отправить сообщение
        """

        print(message)

    def _is_valid_patient_id(self, patient_id):
        """
        Проверка: ID пациента должно быть целове положительное число
        """

        try:
            if int(patient_id) > 0:
                return True
        except ValueError:
            return False
        return False
