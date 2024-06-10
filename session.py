from communicator import Communicator
from command_handler import CommandHandler


class Session:
    """
    Класс, управляет сессией и реагирует на команды
    """

    def __init__(self):
        self.__enabled = True
        self.__communicator = Communicator()
        self.__command_handler = CommandHandler()

    def start(self):
        """
        Запуск программы - основной цикл программы
        """

        while self.__enabled:
            self.__work()

    def __stop(self):
        """
        Остановка программы
        """

        self.__communicator.send_message("Сеанс завершён.")
        self.__enabled = False

    def __work(self):
        """
        Первичная обработка команд, полученных от пользователя
        """

        command = self.__communicator.read_command()
        match command:
            case "узнать статус пациента" | "get status":
                self.__command_handler.get_status()

            case "повысить статус пациента" | "status up":
                self.__command_handler.status_up()

            case "понизить статус пациента" | "status down":
                self.__command_handler.status_down()

            case "выписать пациента" | "discharge":
                self.__command_handler.discharge()

            case "рассчитать статистику" | "calculate statistics":
                self.__command_handler.calculate_statistics()

            case "стоп" | "stop":
                self.__communicator.send_message("Сеанс завершён.")
                self.__enabled = False

            case _:
                self.__communicator.send_message("Неизвестная команда! Попробуйте ещё раз")
