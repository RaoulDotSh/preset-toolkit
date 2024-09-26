# 🎛️ Preset Toolkit

Preset Toolkit is a Python library for working with audio plugin presets and calibration data. It provides tools for reading, writing, and manipulating presets for popular audio plugins, as well as parsing calibration data from audio measurement software.

## 📋 Table of Contents

- [Features](#-features)
- [Limitations](#-limitations)
- [Important Note](#important-note)
- [Installation](#-installation)
- [Usage](#usage)
- [Running the tests](#-running-the-tests)
- [License](#-license)

## 🌟 Features

- Read and write FabFilter Pro-Q 3 preset files
- Parse SoundID Reference export files (Dolby Atmos Renderer export format)

## 🙈 Limitations

FabFilter Pro-Q 3:
- Certain analyzer parameters (analyzer_pre, analyzer_post, analyzer_sidechain, analyzer_range, analyzer_res, analyzer_speed, analyzer_tilt) are supported only in read mode. For an unknown reason, when writing these parameters to a preset, FabFilter Pro-Q 3 does not read them correctly. This is a limitation of the current implementation and how FabFilter Pro-Q 3 interprets the preset file.
- For now, the output gain parameter is not correctly written for values other than 0.
- Some parameters are unknown and marked as unknown1, unknown2, etc. in the code.

## 🚨 Important Note

This code is intended for testing and educational purposes only. It is not intended for production use. The implementation is based on reverse engineering and may not be fully compatible with all versions of the supported software.

## 🚀 Installation

Clone this repository and install the required dependencies:

```bash
git clone https://github.com/RaoulDotSh/preset-toolkit.git
cd preset_toolkit

# [Optional] Create and activate the virtual environment
python -m venv .venv
source .venv/bin/activate

# Install the package
pip install -e .
```

## 🎮 Usage
Here's an example of how to use the `FabFilterPresetManager` class (see examples folder):

### Reading a FabFilter Pro-Q 3 Preset
```python
from preset_toolkit.proq3_preset import FabFilterPresetManager, FabFilterPreset
from preset_toolkit.soundid import SoundIdExport

preset_manager = FabFilterPresetManager()

# Read a preset from a file
default_preset = preset_manager.read_preset("./tests/samples/default_preset.ffp")

# Print the preset
FabFilterPresetManager.print_preset(default_preset)
```

### Writing a FabFilter Pro-Q 3 Preset
```python
from preset_toolkit.proq3_preset import FabFilterPresetManager, FabFilterPreset, ProQFilterType

# Create a new preset
new_preset = FabFilterPreset()

# Modify the preset (example: change the parameters of the first band)
new_preset.bands[0].enabled = True
new_preset.bands[0].gain = 6
new_preset.bands[0].frequency = 4000.0
new_preset.bands[0].q = 2
new_preset.bands[0].filter_type = ProQFilterType.Bell

# Write the preset to a file
preset_manager = FabFilterPresetManager()
preset_manager.write_preset("new_preset.ffp", new_preset)
```

### Reading a SoundID Reference Export

Export a SoundId calibration from menu : export / Dolby Atmos Renderer

```python
from preset_toolkit.soundid import SoundIdExport

soundid_export = SoundIdExport("./tests/samples/soundid.txt")
l_bands, r_bands = soundid_export.get_eq_bands()

print(l_bands)
print(r_bands)
```

## 🧪 Running the tests
```bash
pip install -e .[dev]
pytest
```

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.