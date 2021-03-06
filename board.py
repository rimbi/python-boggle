#!/usr/bin/env python

"""board.py: A package to represent Boggle board."""


class Cell(object):
    """
    Represents a cell on the Boggle board
    """

    def __init__(self, ch, row, column):
        self.ch = ch
        self.row = row
        self.column = column

    def get_coordinates_of_neighbours(self):
        """
        Returns the list of coordinates of the neighbours of the cell
        Example: [(0,0), (0,1)..]
        """
        if self.row > 0:
            yield self.row - 1, self.column
        if self.row < 3:
            yield self.row + 1, self.column
        if self.column > 0:
            yield self.row, self.column - 1
        if self.column < 3:
            yield self.row, self.column + 1
        if self.row > 0 and self.column > 0:
            yield self.row - 1, self.column - 1
        if self.row < 3 and self.column < 3:
            yield self.row + 1, self.column + 1
        if self.row < 3 and self.column > 0:
            yield self.row + 1, self.column - 1
        if self.row > 0 and self.column < 3:
            yield self.row - 1, self.column + 1

    def __eq__(self, o):
        return self.row == o.row and self.column == o.column and self.ch == o.ch

    def __str__(self):
        return '({}, {}) - {}'.format(self.row, self.column, self.ch)

    def __hash__(self):
        return hash(str(self))


class Board(object):
    """
    Represents the Boggle game board
    """

    def __init__(self, config):
        self.config = config

    def _get_cells_of_char(self, c):
        for i, row in enumerate(self.config):
            for j, v in enumerate(row):
                if v == c:
                    yield Cell(c, i, j)

    def _get_neighbour_cells(self, cell):
        for x, y in cell.get_coordinates_of_neighbours():
            yield Cell(self.config[x][y], x, y)

    def get_neighbour_chars(self, c):
        """
        Given a char <c> returns list of its neighbour
        characters on the board
        """
        cells = self._get_cells_of_char(c)
        for cell in cells:
            neighbour_cells = self._get_neighbour_cells(cell)
            for c in neighbour_cells:
                yield c.ch

    def contains(self, word):
        """
        Given a <word> returns True if it exists on the board
        """
        starting_cells = list(self._get_cells_of_char(word[0]))
        if not starting_cells:
            return False
        if len(word) == 1:
            return True
        for c in range(len(word)-1):
            c, n = word[0], word[1]
            if n not in set(self.get_neighbour_chars(c)):
                return False
        return True
