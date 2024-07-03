import pytest
from hospital import Hospital
from errors import PatientNotExists, PatientMaxStatusError, PatientMinStatusError


def test_get_status():
    hospital = Hospital([0, 1, 0])

    assert hospital.get_status(2) == 'Болен'


def test_get_status_when_patient_not_exists():
    hospital = Hospital([0, 1])

    with pytest.raises(PatientNotExists):
        hospital.get_status(3)


def test_get_status_when_patient_is_discharged():
    hospital = Hospital([1, None])

    with pytest.raises(PatientNotExists):
        hospital.get_status(2)


def test_status_up():
    hospital = Hospital([0, 1])

    hospital.status_up(2)

    assert hospital._patients == [0, 2]


def test_status_up_when_patient_has_max_status():
    hospital = Hospital([1, 3])

    with pytest.raises(PatientMaxStatusError):
        hospital.status_up(2)
    assert hospital._patients == [1, 3]


def test_status_up_when_patient_not_exists():
    hospital = Hospital([0, 1])

    with pytest.raises(PatientNotExists):
        hospital.status_up(3)
    assert hospital._patients == [0, 1]


def test_status_up_when_patient_is_already_discharged():
    hospital = Hospital([1, None])

    with pytest.raises(PatientNotExists):
        hospital.status_up(2)
    assert hospital._patients == [1, None]


def test_status_down():
    hospital = Hospital([0, 2])

    hospital.status_down(2)

    assert hospital._patients == [0, 1]


def test_status_down_when_patient_has_min_status():
    hospital = Hospital([0, 2])

    with pytest.raises(PatientMinStatusError):
        hospital.status_down(1)
    assert hospital._patients == [0, 2]


def test_status_down_when_patient_not_exists():
    hospital = Hospital([0, 2])

    with pytest.raises(PatientNotExists):
        hospital.status_down(3)
    assert hospital._patients == [0, 2]


def test_status_down_when_patient_is_already_discharged():
    hospital = Hospital([0, None])

    with pytest.raises(PatientNotExists):
        hospital.status_down(2)
    assert hospital._patients == [0, None]


def test_discharge():
    hospital = Hospital([0, 1])

    hospital.discharge(2)

    assert hospital._patients == [0, None]


def test_discharge_when_patient_not_exists():
    hospital = Hospital([1, 2])

    with pytest.raises(PatientNotExists):
        hospital.discharge(3)
    assert hospital._patients == [1, 2]


def test_discharge_when_patient_is_already_discharged():
    hospital = Hospital([1, None])

    with pytest.raises(PatientNotExists):
        hospital.discharge(2)
    assert hospital._patients == [1, None]


def test_can_status_up():
    hospital = Hospital([1, 2])

    assert hospital.can_status_up(2)


def test_can_status_up_when_patient_has_max_status():
    hospital = Hospital([2, 3])

    assert not hospital.can_status_up(2)


def test_can_status_up_when_patient_not_exists():
    hospital = Hospital([1, 2])

    with pytest.raises(PatientNotExists):
        hospital.can_status_up(3)


def test_can_status_up_when_patient_is_already_discharged():
    hospital = Hospital([1, None])

    with pytest.raises(PatientNotExists):
        hospital.can_status_up(2)


def test_can_status_down():
    hospital = Hospital([1, 2])

    assert hospital.can_status_down(2)


def test_can_status_down_when_patient_has_min_status():
    hospital = Hospital([1, 0])

    assert not hospital.can_status_down(2)


def test_can_status_down_when_patient_not_exists():
    hospital = Hospital([1, 2])

    with pytest.raises(PatientNotExists):
        hospital.can_status_down(3)


def test_can_status_down_when_patient_is_already_discharged():
    hospital = Hospital([1, None])

    with pytest.raises(PatientNotExists):
        hospital.can_status_down(2)


def test_get_statistics():
    hospital = Hospital([3, 1, None, 2, 3, 1, None, 3])

    assert hospital.get_statistics() == {'total': 6,
                                         'hard_ill': 0,
                                         'normal_ill': 2,
                                         'easy_ill': 1,
                                         'ready_for_discharge': 3}
