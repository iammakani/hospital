import pytest
from hospital import Hospital
from errors import PatientNotExists, PatientMaxStatusError


@pytest.fixture()
def hospital():
    return Hospital()


@pytest.mark.parametrize("patient_id", ["1", "100", "200"])
def test_get_status_default(hospital, patient_id):
    assert hospital.get_status(int(patient_id)) == hospital._statuses[1]


def test_get_status_patient_not_exists(hospital):
    with pytest.raises(PatientNotExists):
        hospital.get_status(201)


def test_get_status_discharged_patient_not_exists(hospital):
    with pytest.raises(PatientNotExists):
        hospital.discharge(5)
        hospital.get_status(5)


def test_status_up_one_time(hospital):
    hospital.status_up(2)
    assert hospital.get_status(2) == hospital._statuses[2]


def test_status_up_two_times(hospital):
    hospital.status_up(2)
    hospital.status_up(2)
    assert hospital.get_status(2) == hospital._statuses[3]


def test_status_up_patient_max_status_error(hospital):
    with pytest.raises(PatientMaxStatusError):
        hospital.status_up(100)  # ожидаемое значение статуса = 2
        hospital.status_up(100)  # ожидаемое значение статуса = 3
        hospital.status_up(100)  # тут ожидаем исключение "PatientMaxStatusError"


def test_status_up_patient_not_exists(hospital):
    with pytest.raises(PatientNotExists):
        hospital.status_up(201)


def test_get_statistics_default(hospital):
    assert hospital.get_statistics() == {'total': 200,
                                         'hard_ill': 0,
                                         'normal_ill': 200,
                                         'easy_ill': 0,
                                         'ready_for_discharge': 0}


def test_get_statistics_after_statuses_changes(hospital):
    hospital.status_up(10)
    hospital.status_up(20)
    hospital.status_up(20)
    hospital.status_down(30)
    hospital.discharge(40)
    assert hospital.get_statistics() == {'total': 199,
                                         'hard_ill': 1,
                                         'normal_ill': 196,
                                         'easy_ill': 1,
                                         'ready_for_discharge': 1}
