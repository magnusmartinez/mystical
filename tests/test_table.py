import unittest
from src.pytable import table
from random import random, choice

_t_Table = [
    ['A', 'B', 'C', 'D', 'F', 'G'],
    ['H', 'I', 'J', 'K', 'L', 'M'],
    ['Ñ', 'O', 'P', 'Q', 'R', 'S'],
    ['T', 'V', 'X', 'Y', 'Z', '0'],
    ['1', '2', '3', '4', '5', '6']]


class MyTableTest(unittest.TestCase):

    def test_validate(self):
        self.assertTrue(table.Table.validate(round(random() * 10), round(random() * 10), round(random() * 10)))
        self.assertFalse(table.Table.validate("0", round(-random() * 10), random() * 10))

    def test_row_get(self):
        # args
        row = round((random() * 30) + 1)
        column = round((random() * 30) + 1)
        object_table_0 = table.Table([[0] * column for _ in range(row)])
        object_table_1 = table.Table(row, column)
        object_table_2 = table.Table(row, column, 0)

        self.assertEqual(object_table_0.row, row)
        self.assertEqual(object_table_1.row, row)
        self.assertEqual(object_table_2.row, row)

        # kwargs
        row = round((random() * 30) + 1)
        column = round((random() * 30) + 1)
        object_table_0 = table.Table(table=[[0] * column for _ in range(row)])
        object_table_1 = table.Table(row=row, column=column)
        object_table_2 = table.Table(row=row, column=column, fill=0)

        self.assertEqual(object_table_0.row, row)
        self.assertEqual(object_table_1.row, row)
        self.assertEqual(object_table_2.row, row)

    def test_table_get(self):
        object_table = table.Table(_t_Table)
        self.assertEqual(object_table.table, _t_Table)

        object_table = table.Table(table=_t_Table)
        self.assertEqual(object_table.table, _t_Table)

    def test_table_set(self):
        pass
        # k = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        # raw_table = [(choice(k))] * choice(k)
        #
        # object_table = table.Table(_t_Table)

    def test_row_set(self):
        # ValueError, si value no es de tipo número y mayor que 0
        row = round((random() * 30) + 1)
        _row = round((random() * 10) + 1)
        column = round((random() * 30) + 1)
        object_table = table.Table(row, column)
        object_table.row = _row

        self.assertEqual(object_table.row, _row)

        # Falta probar que devuelva la excepción en el caso que sea requerido.

    def test_column_get(self):
        row = round((random() * 30) + 1)
        column = round((random() * 30) + 1)
        object_table_0 = table.Table([[0] * column for _ in range(row)])
        object_table_1 = table.Table(row, column)
        object_table_2 = table.Table(row, column, 0)

        self.assertEqual(object_table_0.column, column)
        self.assertEqual(object_table_1.column, column)
        self.assertEqual(object_table_2.column, column)

        # kwargs
        row = round((random() * 30) + 1)
        column = round((random() * 30) + 1)
        object_table_0 = table.Table(table=[[0] * column for _ in range(row)])
        object_table_1 = table.Table(row=row, column=column)
        object_table_2 = table.Table(row=row, column=column, fill=0)

        self.assertEqual(object_table_0.column, column)
        self.assertEqual(object_table_1.column, column)
        self.assertEqual(object_table_2.column, column)

    def test_column_set(self):
        pass

    def test_fill(self):
        row = round(random() * 30)
        column = round(random() * 30)
        object_table_0 = table.Table([[0] * column for _ in range(row)])
        object_table_1 = table.Table(row, column)
        object_table_2 = table.Table(row, column, 23)

        self.assertIsNone(object_table_0.fill)
        self.assertEqual(object_table_1.fill, 0)
        self.assertEqual(object_table_2.fill, 23)

    def test_section_up(self):
        object_table = table.Table(_t_Table)
        self.assertEqual(object_table.section_up(3, 2, 4)['content-cell'], 'XPJC')

    def test_section_down(self):
        object_table = table.Table(_t_Table)
        self.assertEqual(object_table.section_down(0, 3, 4)['content-cell'], 'DKQY')

    def test_section_right(self):
        object_table = table.Table(_t_Table)
        self.assertEqual(object_table.section_right(1, 1, 4)['content-cell'], 'IJKL')

    def test_section_left(self):
        object_table = table.Table(_t_Table)
        self.assertEqual(object_table.section_left(2, 5, 4)['content-cell'], 'SRQP')

    def test_section_diagonal_x(self):
        object_table = table.Table(_t_Table)
        self.assertEqual(object_table.section_diagonal_x(3, 1, 4)['content-cell'], 'VPKF')

    def test_section_diagonal_y(self):
        object_table = table.Table(_t_Table)
        self.assertEqual(object_table.section_diagonal_y(4, 5, 4)['content-cell'], '6ZQJ')

    def test_section_diagonal_xr(self):
        object_table = table.Table(_t_Table)
        self.assertEqual(object_table.section_diagonal_xr(0, 5, 4)['content-cell'], 'GLQX')

    def test_section_diagonal_yr(self):
        object_table = table.Table(_t_Table)
        self.assertEqual(object_table.section_diagonal_yr(0, 0, 4)['content-cell'], 'AIPY')

    def test_section(self):
        search = {
            'UP': (3, 2, 4, 'XPJC'),
            'DOWN': (0, 3, 4, 'DKQY'),
            'RIGHT': (1, 1, 4, 'IJKL'),
            'LEFT': (2, 5, 4, 'SRQP'),
            'DIAGONAL-X': (3, 1, 4, 'VPKF'),
            'DIAGONAL-Y': (4, 5, 4, '6ZQJ'),
            'DIAGONAL-XR': (0, 5, 4, 'GLQX'),
            'DIAGONAL-YR': (0, 0, 4, 'AIPY')}
        object_table = table.Table(_t_Table)
        for i in range(7):
            self.assertEqual(
                object_table.section(table.TYPES[i],
                                     search[table.TYPES[i]][0],
                                     search[table.TYPES[i]][1],
                                     search[table.TYPES[i]][2])['content-cell'], search[table.TYPES[i]][3],
                f'La selección en dirección {table.TYPES[i]} falló.'
            )

    def test_get_row(self):
        object_table = table.Table(_t_Table)
        row = round(random() * len(_t_Table) - 1)
        self.assertEqual(object_table.get_row(row), _t_Table[row])

        self.assertIsNone(object_table.get_row(object_table.row + 3))

    def test_get_column(self):
        column = ['G', 'M', 'S', '0', '6']
        object_table = table.Table(_t_Table)
        self.assertEqual(object_table.get_column(5), column)

        self.assertIsNone(object_table.get_column(object_table.column + 3))


if __name__ == '__main__':
    unittest.main()
