from preset_toolkit.proq3_preset import FabFilterPresetManager, FabFilterPreset
from preset_toolkit.soundid import SoundIdExport

preset_manager = FabFilterPresetManager()

# Read a preset from a file
default_preset = preset_manager.read_preset("./tests/samples/default_preset.ffp")

# Print the preset
FabFilterPresetManager.print_preset(default_preset)
