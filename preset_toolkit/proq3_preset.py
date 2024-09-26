import struct
import math
from enum import IntEnum
from dataclasses import dataclass, field
from typing import List, Optional


class ProQFilterType(IntEnum):
    Bell = 0
    LowShelf = 1
    LowCut = 2
    HighShelf = 3
    HighCut = 4
    Notch = 5
    BandPass = 6
    TiltShelf = 7
    FlatTilt = 8


class ProQLPHPSlope(IntEnum):
    Slope6dB_oct = 0
    Slope12dB_oct = 1
    Slope24dB_oct = 2
    Slope48dB_oct = 3


class ProQStereoPlacement(IntEnum):
    Left = 0
    Right = 1
    Stereo = 2


class ProcessMode(IntEnum):
    ZeroLatency = 0
    NaturalPhase = 1
    LinearPhase = 2


class LinearPhaseMode(IntEnum):
    Low = 0
    Med = 1
    High = 2
    VeryHigh = 3
    Max = 4


class AnalyzerResolution(IntEnum):
    Low = 0
    Med = 1
    High = 2
    Max = 3


class AnalyzerRange(IntEnum):
    Range60dB = 0
    Range90dB = 1
    Range120dB = 2


class AnalyzerSpeed(IntEnum):
    VerySlow = 0
    Slow = 1
    Medium = 2
    Fast = 3
    VeryFast = 4


class AnalyzerTilt(IntEnum):
    Tilt0db = 0
    Tilt1dot5db = 1
    Tilt3dB = 2
    Tilt4dot5dB = 3
    Tilt6dB = 4


class AnalyzerSidechain(IntEnum):
    ExternalSpectrumOff = -1
    Sidechain = -2


class DisplayRange(IntEnum):
    DisplayRange3dB = 0
    DisplayRange6dB = 1
    DisplayRange12dB = 2
    DisplayRange30dB = 3


@dataclass
class EQBand:
    enabled: bool = False
    bypass: bool = False
    frequency: float = 1000.0
    gain: float = 0.0
    dyn_range: float = 0.0
    dyn_range_enabled: float = 1.0
    dyn_range_th: float = 1.0
    q: float = 1.0
    filter_type: ProQFilterType = ProQFilterType.Bell
    lp_hp_slope: ProQLPHPSlope = ProQLPHPSlope.Slope12dB_oct
    stereo_placement: ProQStereoPlacement = ProQStereoPlacement.Stereo
    unknown1: float = 1.0
    unknown2: float = 0.0


@dataclass
class GlobalParams:
    process_mode: ProcessMode = ProcessMode.ZeroLatency
    linear_mode_value: LinearPhaseMode = LinearPhaseMode.Med
    gain_scale: float = 1.0
    output_gain: float = 0.0
    output_pan: float = 0.0
    unknown1: float = 0.0
    bypass: bool = False
    phase_invert: bool = False
    auto_gain: bool = False
    analyzer_pre: bool = True
    analyzer_post: bool = True
    analyzer_sidechain: AnalyzerSidechain = AnalyzerSidechain.ExternalSpectrumOff
    analyzer_range: AnalyzerRange = AnalyzerRange.Range90dB
    analyzer_res: AnalyzerResolution = AnalyzerResolution.High
    analyzer_speed: AnalyzerSpeed = AnalyzerSpeed.Medium
    analyzer_tilt: AnalyzerTilt = AnalyzerTilt.Tilt4dot5dB
    unknown2: float = 0.0
    show_collisions: bool = True
    spectrum_grab: bool = True
    display_range: DisplayRange = DisplayRange.DisplayRange12dB
    enable_midi: bool = True
    unknown3: float = 0.0


@dataclass
class FabFilterPreset:
    fxID: str = "FQ3p"
    version: int = 4
    num_params: int = 334
    bands: List[EQBand] = field(default_factory=lambda: [EQBand() for _ in range(24)])
    global_params: GlobalParams = field(default_factory=lambda: GlobalParams())


class FabFilterPresetManager:
    """Manages the reading, writing, and converting of FabFilter Presets."""

    @staticmethod
    def freq_convert(value: float) -> float:
        """Convert frequency to the format used in the preset file."""
        return math.log10(value) / math.log10(2)

    @staticmethod
    def q_convert(value: float) -> float:
        """Convert Q value to the format used in the preset file."""
        return math.log10(value) * 0.312098175 + 0.5

    @staticmethod
    def q_inverse_convert(value: float) -> float:
        """Convert back from the format used in the preset file to Q value."""
        return 10 ** ((value - 0.5) / 0.312098175)

    @staticmethod
    def _read_float(file) -> float:
        """Read a float from a binary file."""
        return struct.unpack("<f", file.read(4))[0]

    @staticmethod
    def _write_float(file, value: float):
        """Write a float to a binary file."""
        file.write(struct.pack("<f", value))

    def _read_bands(self, file) -> List[EQBand]:
        """Reads EQ bands from the file."""
        bands = []
        for _ in range(24):  # Fixed number of bands
            enabled = bool(int(self._read_float(file)))
            bypass = not bool(self._read_float(file))
            frequency = 2 ** self._read_float(file)
            gain = self._read_float(file)
            dyn_range = self._read_float(file)
            dyn_range_enabled = self._read_float(file)
            dyn_range_th = self._read_float(file)
            q = self.q_inverse_convert(self._read_float(file))
            filter_type = ProQFilterType(int(self._read_float(file)))
            lp_hp_slope = ProQLPHPSlope(int(self._read_float(file)))
            stereo_placement = ProQStereoPlacement(int(self._read_float(file)))
            unknown1 = self._read_float(file)
            unknown2 = self._read_float(file)

            bands.append(
                EQBand(
                    enabled=enabled,
                    bypass=bypass,
                    frequency=frequency,
                    gain=gain,
                    dyn_range=dyn_range,
                    dyn_range_enabled=dyn_range_enabled,
                    dyn_range_th=dyn_range_th,
                    q=q,
                    filter_type=filter_type,
                    lp_hp_slope=lp_hp_slope,
                    stereo_placement=stereo_placement,
                    unknown1=unknown1,
                    unknown2=unknown2,
                )
            )
        return bands

    def _write_bands(self, file, bands: List[EQBand]):
        """Writes EQ bands to the file."""
        idx = 0
        for band in bands:
            try:
                self._write_float(file, float(band.enabled))
                self._write_float(file, float(not band.bypass))
                self._write_float(file, self.freq_convert(band.frequency))
                self._write_float(file, band.gain)
                self._write_float(file, band.dyn_range)
                self._write_float(file, band.dyn_range_enabled)
                self._write_float(file, band.dyn_range_th)
                self._write_float(file, self.q_convert(band.q))
                self._write_float(file, float(band.filter_type))
                self._write_float(file, float(band.lp_hp_slope))
                self._write_float(file, float(band.stereo_placement))
                self._write_float(file, band.unknown1)
                self._write_float(file, band.unknown2)
            except Exception as e:
                print(f"Error writing band {idx} to file: {e}")
            idx += 1

    def _read_global_params(self, file) -> GlobalParams:
        """Reads global parameters from the file."""
        return GlobalParams(
            process_mode=ProcessMode(int(self._read_float(file))),
            linear_mode_value=LinearPhaseMode(int(self._read_float(file))),
            gain_scale=self._read_float(file),
            output_gain=self._read_float(file),
            output_pan=self._read_float(file),
            unknown1=self._read_float(file),
            bypass=bool(int(self._read_float(file))),
            phase_invert=bool(int(self._read_float(file))),
            auto_gain=bool(int(self._read_float(file))),
            analyzer_pre=bool(int(self._read_float(file))),
            analyzer_post=bool(int(self._read_float(file))),
            analyzer_sidechain=AnalyzerSidechain(self._read_float(file)),
            analyzer_range=AnalyzerRange(int(self._read_float(file))),
            analyzer_res=AnalyzerResolution(int(self._read_float(file))),
            analyzer_speed=AnalyzerSpeed(int(self._read_float(file))),
            analyzer_tilt=AnalyzerTilt(int(self._read_float(file))),
            unknown2=self._read_float(file),
            show_collisions=bool(int(self._read_float(file))),
            spectrum_grab=bool(int(self._read_float(file))),
            display_range=DisplayRange(int(self._read_float(file))),
            enable_midi=not bool(int(self._read_float(file))),
            unknown3=self._read_float(file),
        )

    def _write_global_params(self, file, params: GlobalParams):
        """Writes global parameters to the file."""
        self._write_float(file, float(params.process_mode))
        self._write_float(file, float(params.linear_mode_value))
        self._write_float(file, params.gain_scale)
        self._write_float(file, params.output_gain)
        self._write_float(file, params.output_pan)
        self._write_float(file, params.unknown1)
        self._write_float(file, float(params.bypass))
        self._write_float(file, float(params.phase_invert))
        self._write_float(file, float(params.auto_gain))
        self._write_float(file, float(params.analyzer_pre))
        self._write_float(file, float(params.analyzer_post))
        self._write_float(file, float(params.analyzer_sidechain))
        self._write_float(file, float(params.analyzer_range))
        self._write_float(file, float(params.analyzer_res))
        self._write_float(file, float(params.analyzer_speed))
        self._write_float(file, float(params.analyzer_tilt))
        self._write_float(file, params.unknown2)
        self._write_float(file, float(params.show_collisions))
        self._write_float(file, float(params.spectrum_grab))
        self._write_float(file, float(params.display_range))
        self._write_float(file, float(not params.enable_midi))
        self._write_float(file, params.unknown3)

    def read_preset(self, file_path: str) -> Optional[FabFilterPreset]:
        """Reads a FabFilter preset from a file."""
        try:
            with open(file_path, "rb") as file:
                fxID = file.read(4).decode("ascii")
                version = struct.unpack("<i", file.read(4))[0]
                num_params = struct.unpack("<i", file.read(4))[0]
                bands = self._read_bands(file)
                global_params = self._read_global_params(file)

                return FabFilterPreset(
                    fxID=fxID,
                    version=version,
                    num_params=num_params,
                    bands=bands,
                    global_params=global_params,
                )

        except (FileNotFoundError, IOError, struct.error) as e:
            print(f"Error reading preset file {file_path}: {e}")
            return None

    def write_preset(self, file_path: str, preset: FabFilterPreset):
        """Writes a FabFilter preset to a file."""
        try:
            with open(file_path, "wb") as file:
                file.write(preset.fxID.encode("ascii"))
                file.write(struct.pack("<i", preset.version))
                file.write(struct.pack("<i", preset.num_params))

                self._write_bands(file, preset.bands)
                self._write_global_params(file, preset.global_params)

                print(f"Preset successfully written to {file_path}")

        except IOError as e:
            print(f"Error writing preset file {file_path}: {e}")
        except Exception as e:
            print(f"Unexpected error writing preset file {file_path}: {e}")

    @staticmethod
    def print_preset(preset: FabFilterPreset):
        idx = 0

        print(f"fxID: {preset.fxID}")
        print(f"version: {preset.version}")
        print(f"num_params: {preset.num_params}")
        print(f"bands: {len(preset.bands)}")

        for band in preset.bands:
            print(
                f"Band {idx} enabled: {band.enabled} bypass: {band.bypass} : unknown 1: {band.unknown1}, unknown 2: {band.unknown2}  Freq {band.frequency}, Gain {band.gain}, Q {band.q}, Filter Type:{band.filter_type}, Stereo Placement:{band.stereo_placement}, dyn_range:{band.dyn_range},  dyn_range_enabled:{band.dyn_range_enabled}, dyn_range_th:{band.dyn_range_th} "
            )
            idx += 1

        print("\nGlobal Parameters:")
        for attr, value in preset.global_params.__dict__.items():
            # Special handling for enum attributes
            if isinstance(value, IntEnum):
                print(
                    f"  {attr}: {value.value} ({value.name})"
                )  # Print both value and name
            else:
                print(f"  {attr}: {value}")
