import pytest
import tempfile
import os
from preset_toolkit.proq3_preset import (
    FabFilterPresetManager,
    FabFilterPreset,
    EQBand,
    GlobalParams,
    ProQFilterType,
    ProcessMode,
    LinearPhaseMode,
    AnalyzerSidechain,
    AnalyzerRange,
    AnalyzerResolution,
    AnalyzerSpeed,
    AnalyzerTilt,
    DisplayRange,
)


@pytest.fixture
def preset_manager():
    return FabFilterPresetManager()


@pytest.fixture
def sample_preset():
    bands = [
        EQBand(
            enabled=True,
            frequency=1000.0,
            gain=2.0,
            q=1.0,
            filter_type=ProQFilterType.Bell,
        ),
        EQBand(
            enabled=False,
            frequency=200.0,
            gain=-3.0,
            q=0.7,
            filter_type=ProQFilterType.LowShelf,
        ),
        EQBand(
            enabled=False,
            frequency=300.0,
            gain=-4.0,
            q=0.6,
            filter_type=ProQFilterType.HighShelf,
        ),
        EQBand(
            enabled=False,
            frequency=400.0,
            gain=-5.0,
            q=0.5,
            filter_type=ProQFilterType.Bell,
        ),
        EQBand(
            enabled=False,
            frequency=500.0,
            gain=-6.0,
            q=0.4,
            filter_type=ProQFilterType.LowShelf,
        ),
        EQBand(
            enabled=False,
            frequency=600.0,
            gain=-7.0,
            q=0.3,
            filter_type=ProQFilterType.HighShelf,
        ),
        EQBand(
            enabled=False,
            frequency=700.0,
            gain=-8.0,
            q=0.2,
            filter_type=ProQFilterType.Bell,
        ),
        EQBand(
            enabled=False,
            frequency=800.0,
            gain=-9.0,
            q=0.1,
            filter_type=ProQFilterType.LowShelf,
        ),
        EQBand(
            enabled=False,
            frequency=900.0,
            gain=-10.0,
            q=1.0,
            filter_type=ProQFilterType.HighShelf,
        ),
        EQBand(
            enabled=False,
            frequency=1000.0,
            gain=-11.0,
            q=1.0,
            filter_type=ProQFilterType.Bell,
        ),
        EQBand(
            enabled=False,
            frequency=1100.0,
            gain=-12.0,
            q=1.0,
            filter_type=ProQFilterType.LowShelf,
        ),
        EQBand(
            enabled=False,
            frequency=1200.0,
            gain=-13.0,
            q=1.0,
            filter_type=ProQFilterType.HighShelf,
        ),
        EQBand(
            enabled=False,
            frequency=1300.0,
            gain=-14.0,
            q=1.0,
            filter_type=ProQFilterType.Bell,
        ),
        EQBand(
            enabled=False,
            frequency=1400.0,
            gain=-15.0,
            q=1.0,
            filter_type=ProQFilterType.LowShelf,
        ),
        EQBand(
            enabled=False,
            frequency=1500.0,
            gain=-16.0,
            q=1.0,
            filter_type=ProQFilterType.HighShelf,
        ),
        EQBand(
            enabled=False,
            frequency=1600.0,
            gain=-17.0,
            q=1.0,
            filter_type=ProQFilterType.Bell,
        ),
        EQBand(
            enabled=False,
            frequency=1700.0,
            gain=-18.0,
            q=1.0,
            filter_type=ProQFilterType.LowShelf,
        ),
        EQBand(
            enabled=False,
            frequency=1800.0,
            gain=-19.0,
            q=1.0,
            filter_type=ProQFilterType.HighShelf,
        ),
        EQBand(
            enabled=False,
            frequency=1900.0,
            gain=-20.0,
            q=1.0,
            filter_type=ProQFilterType.Bell,
        ),
        EQBand(
            enabled=False,
            frequency=2000.0,
            gain=-21.0,
            q=1.0,
            filter_type=ProQFilterType.LowShelf,
        ),
        EQBand(
            enabled=False,
            frequency=2100.0,
            gain=-22.0,
            q=1.0,
            filter_type=ProQFilterType.HighShelf,
        ),
        EQBand(
            enabled=False,
            frequency=2200.0,
            gain=-23.0,
            q=1.0,
            filter_type=ProQFilterType.Bell,
        ),
        EQBand(
            enabled=False,
            frequency=2300.0,
            gain=-24.0,
            q=1.0,
            filter_type=ProQFilterType.LowShelf,
        ),
        EQBand(
            enabled=False,
            frequency=2400.0,
            gain=-25.0,
            q=1.0,
            filter_type=ProQFilterType.HighShelf,
        ),
    ]
    global_params = GlobalParams(
        process_mode=ProcessMode.ZeroLatency,
        linear_mode_value=LinearPhaseMode.Med,
        gain_scale=1.0,
        output_gain=0,
        output_pan=0,
        unknown1=0,
        bypass=False,
        phase_invert=False,
        auto_gain=False,
        analyzer_pre=False,
        analyzer_post=False,
        analyzer_sidechain=AnalyzerSidechain.ExternalSpectrumOff,
        analyzer_range=AnalyzerRange.Range90dB,
        analyzer_res=AnalyzerResolution.Med,
        analyzer_speed=AnalyzerSpeed.Fast,
        analyzer_tilt=AnalyzerTilt.Tilt3dB,
        unknown2=0,
        show_collisions=False,
        spectrum_grab=False,
        display_range=DisplayRange.DisplayRange30dB,
        enable_midi=False,
        unknown3=0,
    )
    return FabFilterPreset(
        fxID="PQ3 ", version=1, num_params=330, bands=bands, global_params=global_params
    )


def test_freq_convert(preset_manager):
    assert pytest.approx(preset_manager.freq_convert(1000)) == 9.965784284662087


def test_q_convert(preset_manager):
    assert pytest.approx(preset_manager.q_convert(1.0)) == 0.5


def test_q_inverse_convert(preset_manager):
    assert pytest.approx(preset_manager.q_inverse_convert(0.5)) == 1.0


def test_write_and_read_preset(preset_manager, sample_preset):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_filename = temp_file.name

    try:
        # Write the preset
        preset_manager.write_preset(temp_filename, sample_preset)

        # Read the preset
        read_preset = preset_manager.read_preset(temp_filename)

        # Check if the read preset matches the original
        assert read_preset.fxID == sample_preset.fxID
        assert read_preset.version == sample_preset.version
        assert read_preset.num_params == sample_preset.num_params

        # Check the first band
        assert read_preset.bands[0].enabled == sample_preset.bands[0].enabled
        assert (
            pytest.approx(read_preset.bands[0].frequency)
            == sample_preset.bands[0].frequency
        )
        assert pytest.approx(read_preset.bands[0].gain) == sample_preset.bands[0].gain
        assert pytest.approx(read_preset.bands[0].q) == sample_preset.bands[0].q
        assert read_preset.bands[0].filter_type == sample_preset.bands[0].filter_type

        # Check global params
        assert (
            read_preset.global_params.process_mode
            == sample_preset.global_params.process_mode
        )
        assert (
            pytest.approx(read_preset.global_params.gain_scale)
            == sample_preset.global_params.gain_scale
        )
        assert read_preset.global_params.bypass == sample_preset.global_params.bypass

    finally:
        os.unlink(temp_filename)


def test_read_nonexistent_file(preset_manager):
    assert preset_manager.read_preset("nonexistent_file.ffp") is None


# Add more tests as needed for other methods and edge cases
