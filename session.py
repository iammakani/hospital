from command_handler import CommandHandler


class Session:
    """
    Класс, описывающий сессию взаимодействия с пользователем
    """

    def __init__(self):
        self.enabled = True
        self.command_handler = CommandHandler(self)

    def start(self):
        """
        Запуск программы - основной цикл программы
        """

        while self.enabled:
            self.read_command()

    def stop(self):
        """
        Остановка программы
        """

        print("Сеанс завершён.")
        self.enabled = False

    def read_command(self):
        """
        Принимаем команду от пользователя и передаем в обработчик команд
        """

        command = (input("Введите команду: "))
        formatted_cmd = command.lower()
        self.command_handler.do_command(formatted_cmd)

    def read_patient_id(self):
        """
        Читаеем ID и проверяем на валидность ID
        ID для работы со списком передается как есть (понижается непосредственно в методах класса Patient)
        """

        patient_id = input("Введите ID пациента: ")
        if self.check_is_valid_patient_id(patient_id):
            return int(patient_id)

    def write(self, text):
        """
        Выводим сообщением пользователю
        """

        print(text)

    def ask_for_discharge(self):
        """
        Запрашиваем у пользователя ответ на вопрос о выписке
        """

        answer = input("Желаете этого клиента выписать? (да/нет): ").lower()
        return answer

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
