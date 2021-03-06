import logging
import sys

from tracker.errors import ValidationError
from tracker.tracker import Tracker

logging.basicConfig(
    format='%(asctime)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S'
)

if __name__ == '__main__':
    tracker = Tracker()
    while True:
        pack = sys.stdin.readline().strip().split()
        try:
            pack[1] = float(pack[1])
            pack[2] = float(pack[2])
        except ValueError or IndexError:
            pass

        try:
            tracker.add_pack(pack)
        except ValidationError:
            logging.warning('Incorrect pack format.')

        print(
            f'steps: {int(tracker.steps)}\n'
            f'kilometers: {round(tracker.kilometers, 2)}\n'
            f'kcal: {round(tracker.kcal, 2)}\n'
        )
