from preset_toolkit.soundid import SoundIdExport

soundid_export = SoundIdExport("./tests/samples/soundid.txt")
l_bands, r_bands = soundid_export.get_eq_bands()

print(l_bands)
print(r_bands)
