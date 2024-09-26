import pytest
from preset_toolkit.soundid import SoundIdExport, EqBand


@pytest.fixture
def sound_id_export():
    return SoundIdExport("tests/samples/soundid.txt")


def test_init(sound_id_export):
    assert sound_id_export.file_path == "tests/samples/soundid.txt"
    assert sound_id_export.l_bands is None
    assert sound_id_export.r_bands is None


def test_parse_eq_bands(sound_id_export):
    sample_data = """
|Freq      |Gain      |
|:---------|:---------|
|40      Hz|4.5     dB|
|50      Hz|5.3     dB|
|100     Hz|1.1     dB|
|800     Hz|-8.2     dB|
    """
    bands = sound_id_export.parse_eq_bands(sample_data)
    assert len(bands) == 4
    assert bands[0] == EqBand(40, 4.5)
    assert bands[1] == EqBand(50, 5.3)
    assert bands[2] == EqBand(100, 1.1)
    assert bands[3] == EqBand(800, -8.2)


def test_extract_calibration_data(sound_id_export):
    sound_id_export.extract_calibration_data()

    assert len(sound_id_export.l_bands) == 27
    assert len(sound_id_export.r_bands) == 27

    # Check a few sample values
    assert sound_id_export.l_bands[0] == EqBand(40, 0)
    assert sound_id_export.l_bands[-1] == EqBand(16000, 6)
    assert sound_id_export.r_bands[0] == EqBand(40, -0.2)
    assert sound_id_export.r_bands[-1] == EqBand(16000, 6)


def test_get_eq_bands(sound_id_export):
    l_bands, r_bands = sound_id_export.get_eq_bands()

    assert len(l_bands) == 27
    assert len(r_bands) == 27

    # Check a few sample values
    assert l_bands[0] == EqBand(40, 0)
    assert l_bands[-1] == EqBand(16000, 6)
    assert r_bands[0] == EqBand(40, -0.2)
    assert r_bands[-1] == EqBand(16000, 6)


def test_verify_all_values(sound_id_export):
    l_bands, r_bands = sound_id_export.get_eq_bands()

    expected_l_bands = [
        EqBand(40, 0),
        EqBand(50, 0.1),
        EqBand(63, 0.4),
        EqBand(80, -5.2),
        EqBand(100, -1.4),
        EqBand(125, -6),
        EqBand(160, -3.8),
        EqBand(200, -5.5),
        EqBand(250, -6),
        EqBand(315, -6),
        EqBand(400, -0.9),
        EqBand(500, 1.1),
        EqBand(630, 3.8),
        EqBand(800, 1.9),
        EqBand(1000, -0.8),
        EqBand(1250, -2),
        EqBand(1600, -2),
        EqBand(2000, 3.9),
        EqBand(2500, 3.4),
        EqBand(3150, 0.2),
        EqBand(4000, 0.9),
        EqBand(5000, -2),
        EqBand(6300, -0.8),
        EqBand(8000, 2.4),
        EqBand(10000, 2.1),
        EqBand(12500, 3.4),
        EqBand(16000, 6),
    ]

    expected_r_bands = [
        EqBand(40, -0.2),
        EqBand(50, -3.7),
        EqBand(63, -0.2),
        EqBand(80, 2.6),
        EqBand(100, 0.5),
        EqBand(125, -6),
        EqBand(160, -6),
        EqBand(200, -3),
        EqBand(250, -4.6),
        EqBand(315, -6),
        EqBand(400, -3.1),
        EqBand(500, 0.5),
        EqBand(630, 1.9),
        EqBand(800, 2.2),
        EqBand(1000, -0.7),
        EqBand(1250, -2.2),
        EqBand(1600, -1.1),
        EqBand(2000, 4.3),
        EqBand(2500, 2),
        EqBand(3150, 0.4),
        EqBand(4000, 1.4),
        EqBand(5000, -1.3),
        EqBand(6300, -0.5),
        EqBand(8000, 1.9),
        EqBand(10000, 2.2),
        EqBand(12500, 3),
        EqBand(16000, 6),
    ]

    assert len(l_bands) == len(expected_l_bands)
    assert len(r_bands) == len(expected_r_bands)

    for actual, expected in zip(l_bands, expected_l_bands):
        assert actual.freq == expected.freq
        assert (
            abs(actual.gain - expected.gain) < 1e-6
        )  # Use small epsilon for float comparison

    for actual, expected in zip(r_bands, expected_r_bands):
        assert actual.freq == expected.freq
        assert (
            abs(actual.gain - expected.gain) < 1e-6
        )  # Use small epsilon for float comparison
