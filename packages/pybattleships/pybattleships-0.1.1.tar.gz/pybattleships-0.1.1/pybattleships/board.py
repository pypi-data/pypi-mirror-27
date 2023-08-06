'''
This module defines the class :class:`Board`.
'''
from collections import OrderedDict
from itertools import dropwhile

from .ship import ShotResult, Ship


class Board:
    '''
    A Board is a 10x10 grid that holds :class:`Ship` s.
    '''
    def __init__(self, ships: [Ship], validate=True):
        '''
        :param [Ship] ships: the ships to place on the Board.
        :param bool validate: whether the board configuration must be valid.

        :raises ValueError: if the board configurations is invalid and `validate`
            is True.
        '''
        self._tries = OrderedDict() # type: [(int, int)] : ShotResult

        self._ships = ships
        self.ships_left = len(ships)

        if not self.valid_board and validate:
            raise ValueError('Invalid ship configuration!')

    @property
    def valid_board(self) -> bool:
        '''
        Returns a boolean indicating whether the Board's state is valid.

        A Board is valid iff it contains ten ships:

         - One Ship with length 5,
         - Two Ships with length 4,
         - Three Ships with Length 3, and
         - Four Ships with Length 2.

        Additionally, the Ships may not overlap each other, or exceed the
        boundaries of the Board.

        :type: bool
        '''
        if len(self._ships) < 10:
            return False

        fields = []
        for ship in self._ships:
            fields += ship.fields

        if len(fields) != len(set(fields)):
            return False

        correct = [2, 2, 2, 2, 3, 3, 3, 4, 4, 5]
        actual = list(map(lambda x: x.size, self._ships))

        if sorted(actual) != correct:
            return False

        return True

    @property
    def is_loss(self) -> bool:
        '''
        Whether all the Ships on the Board have sunk.

        :type: bool
        '''
        return self.ships_left <= 0

    def process_hit(self, x: int, y: int) -> ShotResult:
        '''
        Process a incoming shot by checking it against all Ships on the Board.
        If the position has already been tried, return the previous result.
        '''

        if (x, y) in self._tries:
            return self._tries[(x, y)]

        results = []
        for ship in self._ships:
            results.append(ship.process_hit(x, y))

        theresult = ShotResult.MISS

        hit_ship = list(dropwhile(lambda x: x == ShotResult.MISS, results))
        if hit_ship:
            theresult = hit_ship[0]

            if theresult == ShotResult.SUNK:
                self.ships_left -= 1

        self._tries[(x, y)] = theresult
        return theresult

    def __repr__(self) -> str:
        return self.prettyprint()

    def prettyprint(self, blind: bool = True) -> str:
        '''
        Prints the current state of the Board in a 10x10 character grid.

        :param bool blind: whether the Ships should be hidden.
        '''
        result = [10*['~'] for _ in range(10)]

        if not blind:
            for index, ship in enumerate(self._ships):
                for x, y in ship.fields:
                    result[y][x] = str(index)

        for shot, sresult in self._tries.items():
            x, y = shot
            result[y][x] = sresult.char
        return '\n'.join([''.join(row) for row in result])
