from communicator import Communicator
from command_handler import CommandHandler


class Session:

    def __init__(self):
        self._enabled = True
        self._communicator = Communicator()
        self._command_handler = CommandHandler()

    def start(self, cycles=None):
        enabled = True

        while enabled:
            command = self._communicator.get_command()
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
                    self._command_handler.get_statistics()

                case "стоп" | "stop":
                    self._communicator.send_message("Сеанс завершён.")
                    enabled = False

                case _:
                    self._communicator.send_message("Неизвестная команда! Попробуйте ещё раз")

            if cycles is not None:
                if cycles <= 1:
                    enabled = False
                else:
                    cycles -= 1
