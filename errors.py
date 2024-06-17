class IdValueError(Exception):
    def __str__(self):
        return "Ошибка. ID пациента должно быть числом (целым, положительным)"


class PatientNotExists(Exception):
    def __str__(self):
        return "Ошибка. В больнице нет пациента с таким ID."


class PatientMaxStatusError(Exception):
    def __str__(self):
        return "Ошибка. У пациента уже максимально возможный статус."


class PatientMinStatusError(Exception):
    def __str__(self):
        return "Ошибка. У пациента уже минимально возможный статус"
