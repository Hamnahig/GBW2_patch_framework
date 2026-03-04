"""
emulator.py
-----------
Thin wrapper around PyBoy for ROM loading, frame execution, and shutdown.
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class Emulator:
    """
    Wraps a PyBoy instance.

    Parameters
    ----------
    rom_path : path to the .gbc / .gb ROM file
    headless : run without opening a display window
    speed    : emulation speed multiplier (1=normal, 0=unlimited)
    """

    def __init__(
        self,
        rom_path: str | Path,
        headless: bool = False,
        speed: int = 1,
    ):
        self.rom_path = Path(rom_path)
        self.headless = headless
        self.speed    = speed
        self._pyboy   = None
        self._running = False

    # -----------------------------------------------------------------------
    # Lifecycle
    # -----------------------------------------------------------------------

    def start(self) -> None:
        self._validate_rom()
        self._pyboy = self._create_pyboy()
        self._running = True
        logger.info("Emulator started: %s", self.rom_path)

    def stop(self) -> None:
        self._running = False
        if self._pyboy:
            self._pyboy.stop()
            self._pyboy = None
            logger.info("Emulator stopped.")

    # -----------------------------------------------------------------------
    # Frame execution
    # -----------------------------------------------------------------------

    def tick_once(self) -> bool:
        """Advance one frame. Returns False if the emulator has stopped."""
        if not self._running or not self._pyboy:
            return False
        return self._pyboy.tick(1)

    @property
    def screen_image(self):
        """Current frame as a PIL Image (160×144)."""
        self._require_started()
        return self._pyboy.screen.image

    # -----------------------------------------------------------------------
    # Memory helpers
    # -----------------------------------------------------------------------

    def read_byte(self, address: int) -> int:
        self._require_started()
        return self._pyboy.memory[address]

    def write_byte(self, address: int, value: int) -> None:
        self._require_started()
        self._pyboy.memory[address] = value & 0xFF

    # -----------------------------------------------------------------------
    # Internals
    # -----------------------------------------------------------------------

    def _validate_rom(self) -> None:
        if not self.rom_path.exists():
            raise FileNotFoundError(f"ROM not found: {self.rom_path}")
        if self.rom_path.suffix.lower() not in {".gbc", ".gb"}:
            raise ValueError(f"Unexpected ROM extension '{self.rom_path.suffix}'")
        logger.info(
            "ROM validated: %s (%.1f KB)",
            self.rom_path, self.rom_path.stat().st_size / 1024,
        )

    def _create_pyboy(self):
        try:
            from pyboy import PyBoy
        except ImportError as exc:
            raise ImportError("PyBoy is not installed. Run: pip install pyboy") from exc

        pyboy = PyBoy(str(self.rom_path), window="null" if self.headless else "SDL2")
        if self.speed != 1:
            pyboy.set_emulation_speed(self.speed)
        return pyboy

    def _require_started(self) -> None:
        if not self._running or self._pyboy is None:
            raise RuntimeError("Emulator is not running. Call start() first.")

    # -----------------------------------------------------------------------
    # Context manager
    # -----------------------------------------------------------------------

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *_):
        self.stop()
