from communicator import Communicator
from command_handler import CommandHandler


class Session:
    """
    Класс, управляет сессией и реагирует на команды
    """

    def __init__(self):
        self._enabled = True
        self._communicator = Communicator()
        self._command_handler = CommandHandler()
        self._start()

    def _start(self):
        """
        Запуск программы - основной цикл программы
        """

        while self._enabled:
            self._work()

    def _stop(self):
        """
        Остановка программы
        """

        self._communicator.send_message("Сеанс завершён.")
        self._enabled = False

    def _work(self):
        """
        Первичная обработка команд, полученных от пользователя
        """

        command = self._communicator.read_command()
        match command:
            case "узнать статус пациента" | "get status":
                self._command_handler.get_status()

            case "повысить статус пациента" | "status up":
                self._command_handler.status_up()

            case "понизить статус пациента" | "status down":
                self._command_handler.status_down()

            case "выписать пациента" | "discharge":
                self._command_handler.discharge()

            case "рассчитать статистику" | "calculate statistics":
                self._command_handler.calculate_statistics()

            case "стоп" | "stop":
                self._communicator.send_message("Сеанс завершён.")
                self._enabled = False

            case _:
                self._communicator.send_message("Неизвестная команда! Попробуйте ещё раз")
