import sys
from gbc_patcher.gui import launch_gui

rom_path = sys.argv[1] if len(sys.argv) > 1 else None
launch_gui(rom_path=rom_path)
