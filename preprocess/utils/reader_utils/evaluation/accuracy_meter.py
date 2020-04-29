import logging
from collections import namedtuple

logger = logging.getLogger(__name__)

ScoreRecord = namedtuple('ScoreRecord', 'row, col, score, length')


class AccuracyMeter:
    def __init__(self):
        """ A class for calculating accuracy metric.
        """
        self.records = []

    def __str__(self):
        return '{0:.2f}% by field'.format(self.get_acc_by_field() * 100)

    def add(self, row: int, col: int, score: float, length: int = 0):
        """ Add a record for calculating accuracy metric
        :param row: row index
        :param col: column index
        :param length: length of the text, default = 0 - not affect acc_by_char
        :param score: metric representing the accuracy
        """
        self.records.append(ScoreRecord(row, col, score, length))

    def get_acc_by_char(self, row=None, col=None) -> float:
        """ Get accuracy by char of the given `row` and `col`.
        :param row: row index, default: None.
        :param col: column index, default: None.
        :return: the accuracy by char of a record specified by `row` and `col`.
            - if row == None: return accuracy for the whole column.
            - if col == None: return accuracy for the whole row.
            - if row == col == None: return the overall accuracy.
        """
        try:
            if row is None and col is None:
                return sum([r.score * r.length for r in self.records]) / sum(
                    [r.length for r in self.records])

            if row is None or col is None:
                score = 0
                length = 0
                for r in self.records:
                    if (r.col == col) if row is None else (r.row == row):
                        score += r.score * r.length
                        length += r.length
                return score / length

            for r in self.records:
                if r.row == row and r.col == col:
                    return r.score
            else:
                raise IndexError(f'Cannot found record with at row: {row}, col: {col}')
        except ZeroDivisionError as e:
            logger.warning(f'Cannot found any matching record with row: {row}, col: {col}')
            return 0

    def get_acc_by_field(self, row=None, col=None, threshold: float = 0.99) -> float:
        """ Get accuracy by field of the given `row` and `col`.
        :param row: row index, default: None.
        :param col: column index, default: None.
        :param threshold: threshold to convert by char accuracy to by field accuracy
        :return: the accuracy by field of a record specified by `row` and `col`.
            - if row == None: return accuracy for the whole column.
            - if col == None: return accuracy for the whole row.
            - if row == col == None: return the overall accuracy.
        """

        def to_field_acc(score):
            return 1 if score > threshold else 0

        try:
            if row is None and col is None:
                scores = [to_field_acc(r.score) for r in self.records if r.length]
                if scores:
                    return sum(scores) / len(scores)
                else:
                    return 1

            if row is None or col is None:
                scores = [to_field_acc(r.score) for r in self.records if
                          r.length > 0 and ((r.col == col) if row is None else (r.row == row))]

                if scores:
                    return sum(scores) / len(scores)
                else:
                    return 1

            for r in self.records:
                if r.row == row and r.col == col:
                    return to_field_acc(r.score)
            else:
                raise IndexError(f'Cannot found record with at row: {row}, col: {col}')
        except ZeroDivisionError as e:
            logger.warning(f'Cannot found any matching record with row: {row}, col: {col}')
            return 0
