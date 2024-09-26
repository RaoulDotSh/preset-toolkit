from preset_toolkit.proq3_preset import (
    FabFilterPresetManager,
    FabFilterPreset,
    ProQFilterType,
)

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
