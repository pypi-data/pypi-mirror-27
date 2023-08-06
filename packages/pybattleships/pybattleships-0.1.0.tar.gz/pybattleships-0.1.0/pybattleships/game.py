'''
This module defines the class :class:`Game`.
'''
from .board import Board
from .ship import Ship, ShotResult

class Game:
    '''
    A Game represents a game of Battleships between two players.
    '''

    def __init__(self, player1: str, player2: str):
        '''
        :param str player1: the identifier to use for player one.
        :param str player2: the identifier to use for player two.
        '''

        self.turn = 0
        self.player1 = player1
        self.player2 = player2

        self.players = {
            player1: 1,
            player2: 2,
            1: player1,
            0: player2
        }

        self.boards = {
            player1: None,
            player2: None
        }

    def setup_board(self, player_id: str, ships: [Ship]) -> bool:
        '''
        Create a Board from the given set of ships, assert validity and
        register the Board with the Game if it is valid.

        Returns False if the Board is invalid, and will then not accept the
        Board.

        :param str player_id: the player identifier to set the board for.
        :param [Ship] ships: the list of Ships to populate the Board with.

        :raises AssertionError: if the passed player identifier is unknown.
        '''

        try:
            board = Board(ships)
        except ValueError:
            # Board invalid, abort
            return False

        assert player_id in self.boards

        self.boards[player_id] = board
        return True


    def register_board(self, player_id: str, board: Board):
        '''
        Register a board object to a player

        :param str player_id: the player identifier to set the board for.
        :param Board board: the board to register to the player.

        :raises AssertionError: if the passed player identifier is unknown.
        '''

        assert player_id in self.boards
        self.boards[player_id] = board


    def start_game(self) -> bool:
        '''
        Asserts both boards are present and valid, starts the Game, and gives
        the turn to player 1.

        Returns False if one or more of the Boards is absent or invalid, True
        on success.
        '''

        for _player, board in self.boards.items():
            if not (board and board.valid_board):
                return False

        self.turn = 1
        return True

    @property
    def current_player(self) -> str:
        '''
        Returns the identifier of the player on move.

        :type: str
        '''

        if self.turn == 0:
            return None

        return self.players[self.turn % 2]

    @property
    def current_adversary(self) -> str:
        '''
        Returns the identifier of the player not on move.

        :type: str
        '''

        if self.turn == 0:
            return None

        return self.players[(self.turn + 1) % 2]

    def process_fire(self, x: int, y: int) -> ShotResult:
        '''
        Process a player's input: fire at the opponent's Board, and return the
        result of the shot.

        Returns :attr:`ShotResult.LOSS` if this shot makes the opponent lose
        the game.

        :param int x: the x-coordinate to fire at.
        :param int y: the y-coordinate to fire at.
        '''

        player_id = self.current_adversary
        board = self.boards[player_id]
        result = board.process_hit(x, y)
        self.turn += 1

        if result == ShotResult.SUNK and board.is_loss:
            return ShotResult.LOSS

        return result
