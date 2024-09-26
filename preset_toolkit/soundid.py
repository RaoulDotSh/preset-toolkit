from dataclasses import dataclass
import re


@dataclass
class EqBand:
    freq: float
    gain: float


class SoundIdExport:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.l_bands = None
        self.r_bands = None

    def parse_eq_bands(self, data: str) -> list[EqBand]:
        bands = []
        for line in data.strip().split("\n")[2:]:  # Skip the header lines
            match = re.match(r"\|(\d+)\s+Hz\|([-\d.]+)\s+dB\|", line)
            if match:
                freq = float(match.group(1))
                gain = float(match.group(2))
                bands.append(EqBand(freq, gain))
        return bands

    def extract_calibration_data(self):
        with open(self.file_path, "r") as file:
            content = file.read()

        # Extract L channel and R channel EQ data using regex
        l_channel_data = re.search(
            r"L channel calibration:\s*Delay:.*?Gain:.*?\n\n\|Freq\s+\|Gain\s+.*?\n(\|.*?\n)+",
            content,
            re.DOTALL,
        )
        r_channel_data = re.search(
            r"R channel calibration:\s*Delay:.*?Gain:.*?\n\n\|Freq\s+\|Gain\s+.*?\n(\|.*?\n)+",
            content,
            re.DOTALL,
        )

        if l_channel_data and r_channel_data:
            l_channel_data_str = l_channel_data.group(0)
            r_channel_data_str = r_channel_data.group(0)

            self.l_bands = self.parse_eq_bands(l_channel_data_str)
            self.r_bands = self.parse_eq_bands(r_channel_data_str)
        else:
            raise ValueError("Could not find the required EQ band data in the file.")

    def get_eq_bands(self):
        if self.l_bands is None or self.r_bands is None:
            try:
                self.extract_calibration_data()
            except ValueError as e:
                print(e)
                return None, None
        return self.l_bands, self.r_bands
