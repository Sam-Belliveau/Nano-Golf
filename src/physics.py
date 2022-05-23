from __future__ import annotations

from electron import Electron


class Force:
    def apply(self, electron: Electron, dt: float) -> None: raise NotImplementedError
