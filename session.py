from communicator import Communicator
from command_handler import CommandHandler


class Session:

    def __init__(self, communicator=None, command_handler=None):
        self._communicator = communicator or Communicator()
        self._command_handler = command_handler or CommandHandler()

    def start(self):
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
