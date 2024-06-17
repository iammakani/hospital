from errors import IdValueError


class Communicator:

    def get_command(self):

        command = input("Введите команду: ")
        formatted_command = command.lower()
        return formatted_command

    def get_patient_id(self):

        patient_id = input("Введите ID пациента: ")
        if self._is_valid_patient_id(patient_id):
            return int(patient_id)
        else:
            raise IdValueError

    def will_patient_discharge(self):

        answer = input(f"Желаете этого клиента выписать? (да/нет): ").lower()
        if answer == 'да':
            return True
        return False

    def send_message(self, message):

        print(message)

    def _is_valid_patient_id(self, patient_id):

        try:
            if int(patient_id) > 0:
                return True
        except ValueError:
            return False
        return False
