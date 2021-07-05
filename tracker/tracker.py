import re
from datetime import time

from tracker.errors import ValidationError


class Pack:
    def __init__(self, pack: tuple):
        self._is_valid = False
        if self.validate_pack(pack):
            t = time.fromisoformat(pack[0])
            self.timestamp = t.hour * 3600 + t.minute * 60 + t.second
            self.steps = pack[1]
            self.pulse = pack[2]
            self._is_valid = True

    @staticmethod
    def validate_pack(pack) -> bool:
        if len(pack) != 3:
            return False

        if not re.fullmatch(r'\d{2}:\d{2}:\d{2}', pack[0]):
            return False

        if not isinstance(pack[1], (int, float)):
            return False

        if not isinstance(pack[2], (int, float)):
            return False

        return True

    def is_valid(self, raise_exception: bool = False):
        if self._is_valid:
            return True

        if raise_exception:
            raise ValidationError
        return False


class Tracker:
    def __init__(self, mass: float = 80):
        """
        :param mass: Human being mass in kilograms.
        """
        self._packs = [
            Pack(('00:00:00', 0, 0)),
        ]
        self._steps = 0
        self._kcal = 0
        self._mass = mass

    def _calculate_kcal(self, timedelta, pulse):
        minutes = timedelta / 60
        return 0.014 * self._mass * minutes * (0.12 * pulse - 7)

    @property
    def kcal(self) -> float:
        return self._kcal

    @property
    def kilometers(self) -> float:
        return self._steps / 1429

    @property
    def steps(self) -> int:
        return self._steps

    def add_pack(self, pack: tuple):
        pack = Pack(pack)
        if pack.is_valid(raise_exception=True):
            if pack.timestamp < self._packs[-1].timestamp:
                raise ValidationError

            self._steps += pack.steps
            self._kcal += self._calculate_kcal(
                timedelta=pack.timestamp - self._packs[-1].timestamp,
                pulse=pack.pulse,
            )
            self._packs.append(pack)
