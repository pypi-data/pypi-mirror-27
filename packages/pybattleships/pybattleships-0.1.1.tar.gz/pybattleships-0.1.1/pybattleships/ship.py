'''
This module defines the class :class:`Ship`, and a helper class,
:class:`ShotResult`.
'''
import enum
import re


class ShotResult(enum.IntEnum):
    ''' A ShotResult represents the result of firing on a :class:`Ship`. '''
    MISS = 0
    ''' Shot did not hit Ship. '''
    HIT = 1
    ''' Shot hit Ship, did not sink yet. '''
    SUNK = 2
    ''' Shot hit Ship, Ship sunk. '''
    LOSS = 3
    ''' Shot hit Ship, Ship sunk, Ship was last Ship on Board. '''

    @property
    def char(self) -> str:
        ''' Return the character to use when pretty-printing. '''
        return ['*', 'X', '#', 'B^u'][self]

class Ship:
    '''
    A Ship represents a Battleship piece.
    '''

    def __init__(self, x: int, y: int, horizontal: bool, size: int):
        '''
        :param int x: The x-coordinate of the top-left square.
        :param int y: The y-coordinate of the top-left square.
        :param bool horizontal: Whether the ship is positioned horizontally
            (True), or vertically (False).
        :param int size: The number of squares the Ship occupies.

        :raises ValueError: if the Ship is placed outside of the Board.
        :raises ValueError: if the Ship has an invalid `size`.
        '''
        self._x = x
        self._y = y

        self._horizontal = horizontal # type: bool
        self._size = size

        self._hit = 0

        # Check boundaries
        out_of_bounds = any(
            [
                horizontal and (x+size-1 >= 10),
                not horizontal and (y+size-1 >= 10),
                x < 0,
                y < 0
            ]
        )
        if out_of_bounds:
            raise ValueError(
                "Can't place a Ship outside of the board: {}, {}".format(
                    x+size, y)
                )

        if size <= 1 or size > 5:
            raise ValueError("Ship size outside [2..5]: {}".format(size))

    @property
    def sunk(self) -> bool:
        '''
        A ship sinks when every position is hit, which means it has been hit
        `size` times. Once the ship has sunk, this property is True.

        :type: bool
        '''
        return self._hit >= self._size

    @property
    def fields(self) -> [(int, int)]:
        '''
        Return the list of fields this Ship occupies as a list of (x, y)
        tuples.

        :type: [(int, int)]
        '''
        pos_x, pos_y = self._x, self._y
        result = [(pos_x, pos_y)]

        if self._horizontal:
            deltax = 1 # Go left
            deltay = 0
        else:
            deltax = 0
            deltay = 1 # Go down

        for _ in range(self._size-1):
            pos_x += deltax
            pos_y += deltay

            result.append(
                (pos_x, pos_y)
            )

        return result

    def process_hit(self, x: int, y: int) -> ShotResult:
        '''
        Assert that the given shot was on this Ship, if so, increase the
        hitcounter. Return whether the Ship was missed, hit, or sunk.
        '''

        hit_ship = \
            all([
                self._horizontal,
                y == self._y,
                x >= self._x,
                x < (self._x + self._size)
            ]) or \
            all([
                not self._horizontal,
                x == self._x,
                y >= self._y,
                y < (self._y + self._size)
            ])

        if hit_ship:
            self._hit += 1
            if self.sunk:
                return ShotResult.SUNK
            return ShotResult.HIT

        return ShotResult.MISS

    @property
    def size(self):
        '''
        Return the number of fields the Ship occupies.

        :type: int
        '''
        return self._size

    notational_pattern = r'''
\(
(?P<x>[A-Ja-j])
(?P<y>(10|[1-9])),\s*
(?P<orientation>[hHvV]),\s*
(?P<size>[2-5])
\)
    '''
    notational_regex = re.compile(notational_pattern, re.X)

    @classmethod
    def parse_notation(cls, notation: str):
        '''
        Parse a written representation of a Ship, like `(A1, h, 2)`,
        return a new Ship on this position.

        :param str notation: the notation to parse.
        :raises ValueError: if the passed notation is invalid.
        '''

        match = cls.notational_regex.match(notation)

        if not match:
            raise ValueError("Invalid notation!")

        x = ord(match.group('x').upper()) - ord('A')
        y = int(match.group('y'))         - 1

        horizontal = match.group('orientation').upper() == 'H'

        size = int(match.group('size'))

        return Ship(x, y, horizontal, size)

    def __repr__(self):
        return '<Ship({}, {}, {}, {})>'.format(
            self._x, self._y,
            self._horizontal, self._size
        )

    shot_pattern = r'''
(?P<x>[A-Ja-j])
(?P<y>(10|[1-9]))
    '''
    shot_regex = re.compile(shot_pattern, re.X)

    @classmethod
    def parse_shot_notation(cls, notation: str) -> (int, int):
        '''
        Parse a single location on the board in traditional Battleships
        notation (A1-J10), and return a (x, y)-tuple of indexes on the Board.

        :param str notation: the notations to parse.

        :raises ValueError: if the passed notation is invalid.
        '''

        match = cls.shot_regex.match(notation)

        if not match:
            raise ValueError("Invalid notation!")

        x = ord(match.group('x').upper()) - ord('A')
        y = int(match.group('y'))         - 1

        return (x, y)
