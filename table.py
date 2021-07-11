"""
Módulo Python para el procesamiento de tablas, permite la selección de celdas en
cualquier dirección.
"""
TYPES = ('UP', 'DOWN', 'RIGHT', 'LEFT', 'DIAGONAL-X', 'DIAGONAL-Y', 'DIAGONAL-XR', 'DIAGONAL-YR')
UP = 'UP'
DOWN = 'DOWN'
RIGHT = 'RIGHT'
LEFT = 'LEFT'
DIAGONAL_X = 'DIAGONAL-X'
DIAGONAL_Y = 'DIAGONAL-Y'
DIAGONAL_XR = 'DIAGONAL-XR'
DIAGONAL_YR = 'DIAGONAL-YR'

__author__ = "Elías Martínez (Magnus)"
__copyright__ = "Copyright 2021"
__version__ = "1.0"
__name__ = 'tabla'

from tabulate import tabulate


class AnyError(Exception):
    """BaseError class for all Exceptions of type Tabla"""
    pass


class TableSectionError(AnyError):
    """Lanzada cuando la selección que se quiere obtener de la tabla es inadmitida"""

    def __init__(self, start='', stop='', message='Rango de selección incorrecto'):
        self.message = message
        self.start = start
        self.stop = stop

    def __str__(self):
        if self.start and self.stop:
            return f"start: {self.start} - stop: {self.stop} >> {self.message}"
        else:
            return f"{self.message}"


class TableStructureError(AnyError):
    """alzada al intentar crear una estructura de tabla no correcta"""

    def __init__(self, message="Error en la estructura de la tabla"):
        self.msg = message

    def __str__(self):
        return self.msg


class Table:
    """Permita la creación y manipulación tablas.

    Argumentos:
    Si el número de argumentos es 3, el primero será el número de filas de la tabla,
    el segundo será el número de columnas de la tabla y el tercero será el contenido de las celdas de la tabla.
    #>>>print(Table(2, 5, 'r'))
            +---+---+---+---+---+
            | r | r | r | r | r |
            +---+---+---+---+---+
            | r | r | r | r | r |
            +---+---+---+---+---+

    Si el número de argumentos es 2, el primero será el número de filas y
    el segundo será el número de columnas de la tabla.
    #>>>print(Table(2, 3))
            +---+---+---+
            | 0 | 0 | 0 |
            +---+---+---+
            | 0 | 0 | 0 |
            +---+---+---+

    Si el número de argumentos es igual a 1, será ser la representación de una tabla con listas.
    El llenado de las celdas es albitrario.
    #>>>print(Table([[2, True, 'Python'], [0.2, '0', 4], ['Python', 'Es', 'Bueno']]))
            +--------+------+--------+
            | 2      | True | Python |
            +--------+------+--------+
            | 0.2    | 0    | 4      |
            +--------+------+--------+
            | Python | Es   | Bueno  |
            +--------+------+--------+

    Si se pasan argumentos por referencia, row y column corresponden al número de filas y columnas respectivamente.
    #>>>print(Table(row=2, column=3))
            +---+---+---+
            | 0 | 0 | 0 |
            +---+---+---+
            | 0 | 0 | 0 |
            +---+---+---+

    Opcionalmente, para establecer un contenido de celdas utilice fill.
    #>>>print(Table(row=2, column=3, fill=2.4))
            +-----+-----+-----+
            | 2.4 | 2.4 | 2.4 |
            +-----+-----+-----+
            | 2.4 | 2.4 | 2.4 |
            +-----+-----+-----+

    Para utilizar una tabla previamente creada, utilice table.
    #>>>print(Table(table=[[2, True, 'Python'], [0.2, '0', 4], ['Python', 'Es', 'Bueno']]))
            +--------+------+--------+
            | 2      | True | Python |
            +--------+------+--------+
            | 0.2    | 0    | 4      |
            +--------+------+--------+
            | Python | Es   | Bueno  |
            +--------+------+--------+
    """

    def __init__(self, *args, **kwargs):
        self.__row = 0
        self.__column = 0
        self.__fill = '0'
        self.__type = ('UP', 'DOWN', 'RIGHT', 'LEFT', 'DIAGONAL-X', 'DIAGONAL-Y', 'DIAGONAL-XR', 'DIAGONAL-YR')
        self.__table = None
        self.__make(*args, **kwargs)

    def __make(self, *args, **kwargs):
        """Construye la tabla en base a los argumentos pasados"""
        if args and kwargs:
            raise ValueError('No se permite el paso de parametros por posicion y por referencia de forma simultanea')

        if len(args):
            if len(args) == 3:
                self.__fill = args[2]
                self.row = args[0]
                self.column = args[1]
                self.__table = [[self.__fill] * self.column for _ in range(self.row)]

            elif len(args) == 2:
                self.row = args[0]
                self.column = args[1]
                self.__table = [[self.__fill] * self.column for _ in range(self.row)]

            elif len(args) == 1:
                self.table = args[0]
            else:
                raise ValueError(f'se esperaban 3, 2 o 1 argumentos y pasaraon {len(args)}: {args} ')

        if kwargs:
            try:
                self.table = kwargs['table']
            except KeyError:
                try:
                    self.__fill = kwargs['fill']
                except KeyError:
                    pass

                try:
                    self.row = kwargs['row']
                except KeyError:
                    raise KeyError(f'Numero de filas no establecido')
                try:
                    self.column = kwargs['column']
                except KeyError:
                    raise KeyError(f'Numero de columnas no establecido')

                self.__table = [[self.__fill] * self.column for _ in range(self.row)]

    def __str__(self):
        # In [10]: tabulate.tabulate([[2, 2],[3, 4]], tablefmt="grid")
        # Out[10]: '+---+---+\n| 2 | 2 |\n+---+---+\n| 3 | 4 |\n+---+---+'
        return tabulate(self.__table, tablefmt="grid")

    def __repr__(self):
        return f"{self.__class__.__name__}({self.row}, {self.column}, {self.fill})"

    @property
    def row(self) -> int:
        """Devuelve el número de filas de la tabla."""
        return self.__row

    @property
    def column(self) -> int:
        """Devuelve el número de columnas de la tabla."""
        return self.__column

    @property
    def fill(self):
        """Devuelve el tipo de llenado que tiene la tabla.
        Devuelve None, no cuando la tabla es pasada ya construida.
        """
        return self.__fill

    @property
    def table(self) -> list[[list, ..., list]]:
        """Devuelve la tabla."""
        return self.__table

    @table.setter
    def table(self, value):
        """Establece una tabla previamente construida.

        Parámetros (value)
            QUÉ SON:
                value: es una matriz previamente construida.

            CÓMO SON:
                1. La tabla debe ser de tipo lista y todos elementos también
                2. Las dimensiones mínimas admitidas son 1x1
                3. El número de celdas en cada fila debe ser común.

        EXCEPCIONES:
            TableStructureError, si no se cumple alguno de los puntos anteriores.

        """
        if isinstance(value, list) and not any(map(lambda x: not isinstance(x, list), value)):
            _row = len(value[0])
            for row in value:
                if len(row) <= 0 or _row != len(row):
                    raise TableStructureError(f'Las dimensiones de la tabla no son correctas.')

            self.__table = value
            self.__row = len(self.__table)
            self.__column = len(self.__table[0])
            self.__fill = None
        else:
            raise TableStructureError

    @row.setter
    def row(self, value):
        """Actualiza el número de filas de la tabla.

        Excepciones:
             ValueError, si value no es de tipo número y mayor que 0
        """
        if isinstance(value, int) and value > 0:
            self.__row = value
            self.__table = [[self.fill] * self.column for _ in range(self.row)]
        else:
            raise ValueError("row debe ser un numero y deber mayor que 0")

    @column.setter
    def column(self, value):
        """Actualiza el número de columnas de la tabla.

        Excepciones:
             ValueError, si value no es de tipo número y mayor que 0
        """
        if isinstance(value, int) and value > 0:
            self.__column = value
            self.__table = [[self.fill] * self.column for _ in range(self.row)]
        else:
            raise ValueError("column debe ser un número y debe ser mayor que 0")

    def section_up(self, row: int, column: int, cell: int) -> dict:
        """
        DESCRIPCIÓN `section_up`:
            La selección en up se realiza sobre la tabla con sentido al N
                Noroeste    N   Noreste
                        O   +   E
                Suroeste    S   Sureste

        PARÁMETROS (row, column, cell):
            CÓMO SON:
                row: debe ser de tipo int y ser mayor o igual a 0
                column: debe ser de tipo int y ser mayor o igual a 0
                cell: debe ser de tipo ini y ser mayor o igual a 0

            QUÉ SON:
                row: fila inicial de la selección
                column: columna inicial de la selección
                cell: la cantidad de celdas a seleccionar
        RETORNO:
            Un diccionario con las siguientes llaves:
                * type: La orientación de la selección
                * position: Las posiciones correspondientes a la selección
                * content-cell: La unión del contenido de las celdas seleccionadas

        EXCEPCIONES (ValueError):
            ValueError, si validate(row, column, cell) es Falso
            TableSectionError, si la selección es incorrecta, es decir, que en la tabla no es posible realizar
                        ese tipo de selección
        """
        if not self.validate(row, column, cell):
            raise ValueError(
                'Los parámetros no son válidos.'
            )
        output = {'type': self.__type[0], 'position': [], 'content-cell': ''}
        for i in range(cell):
            if 0 > row - i:
                raise TableSectionError()
            output['position'].append((row - i, column))
            output['content-cell'] += self.table[row - i][column]
        return output

    def section_down(self, row: int, column: int, cell: int) -> dict:
        """
        DESCRIPCIÓN `section_down`:
            La selección en down se realiza sobre la tabla con sentido al S
                Noroeste    N   Noreste
                        O   +   E
                Suroeste    S   Sureste

        PARÁMETROS (row, column, cell):
            CÓMO SON:
                row: debe ser de tipo int y ser mayor o igual a 0
                column: debe ser de tipo int y ser mayor o igual a 0
                cell: debe ser de tipo ini y ser mayor o igual a 0

            QUÉ SON:
                row: fila inicial de la selección
                column: columna inicial de la selección
                cell: la cantidad de celdas a seleccionar
        RETORNO:
            Un diccionario con las siguientes llaves:
                * type: La orientación de la selección
                * position: Las posiciones correspondientes a la selección
                * content-cell: La unión del contenido de las celdas seleccionadas

        EXCEPCIONES (ValueError):
            ValueError, si validate(row, column, cell) es Falso
            TableSectionError, si la selección es incorrecta, es decir, que en la tabla no es posible realizar
                        ese tipo de selección
        """
        if not self.validate(row, column, cell):
            raise ValueError(
                'Los parámetros no son válidos.'
            )
        output = {'type': self.__type[1], 'position': [], 'content-cell': ''}
        for i in range(cell):
            try:
                output['position'].append((row + i, column))
                output['content-cell'] += self.table[row + i][column]
            except IndexError:
                raise TableSectionError("Limites excedidos.")
        return output

    def section_right(self, row: int, column: int, cell: int) -> dict:
        """
        DESCRIPCIÓN `section_right`:
            La selección en right se realiza sobre la tabla con sentido al E
                Noroeste    N   Noreste
                        O   +   E
                Suroeste    S   Sureste

        PARÁMETROS (row, column, cell):
            CÓMO SON:
                row: debe ser de tipo int y ser mayor o igual a 0
                column: debe ser de tipo int y ser mayor o igual a 0
                cell: debe ser de tipo ini y ser mayor o igual a 0

            QUÉ SON:
                row: fila inicial de la selección
                column: columna inicial de la selección
                cell: la cantidad de celdas a seleccionar
        RETORNO:
            Un diccionario con las siguientes llaves:
                * type: La orientación de la selección
                * position: Las posiciones correspondientes a la selección
                * content-cell: La unión del contenido de las celdas seleccionadas

        EXCEPCIONES (ValueError):
            ValueError, si validate(row, column, cell) es Falso
            TableSectionError, si la selección es incorrecta, es decir, que en la tabla no es posible realizar
                        ese tipo de selección
        """
        if not self.validate(row, column, cell):
            raise ValueError(
                'Los parámetros no son válidos.'
            )
        output = {'type': self.__type[2], 'position': [], 'content-cell': ''}
        for i in range(cell):
            try:
                output['position'].append((row, column + i))
                output['content-cell'] += self.table[row][column + i]
            except IndexError:
                raise TableSectionError()
        return output

    def section_left(self, row: int, column: int, cell: int) -> dict:
        """
        DESCRIPCIÓN `section_left`:
            La selección en left se realiza sobre la tabla con sentido al O
                Noroeste    N   Noreste
                        O   +   E
                Suroeste    S   Sureste

        PARÁMETROS (row, column, cell):
            CÓMO SON:
                row: debe ser de tipo int y ser mayor o igual a 0
                column: debe ser de tipo int y ser mayor o igual a 0
                cell: debe ser de tipo ini y ser mayor o igual a 0

            QUÉ SON:
                row: fila inicial de la selección
                column: columna inicial de la selección
                cell: la cantidad de celdas a seleccionar
        RETORNO:
            Un diccionario con las siguientes llaves:
                * type: La orientación de la selección
                * position: Las posiciones correspondientes a la selección
                * content-cell: La unión del contenido de las celdas seleccionadas

        EXCEPCIONES (ValueError):
            ValueError, si validate(row, column, cell) es Falso
            TableSectionError, si la selección es incorrecta, es decir, que en la tabla no es posible realizar
                        ese tipo de selección
        """
        if not self.validate(row, column, cell):
            raise ValueError(
                'Los parámetros no son válidos.'
            )
        output = {'type': self.__type[3], 'position': [], 'content-cell': ''}
        for i in range(cell):
            if column - i < 0:
                raise TableSectionError()
            output['position'].append((row, column - i))
            output['content-cell'] += self.table[row][column - i]
        return output

    def section_diagonal_x(self, row: int, column: int, cell: int) -> dict:
        """
        DESCRIPCIÓN `section_diagonal_x`:
            La selección en diagonal-x se realiza sobre la tabla con sentido al Noreste
                Noroeste    N   Noreste
                        O   +   E
                Suroeste    S   Sureste

        PARÁMETROS (row, column, cell):
            CÓMO SON:
                row: debe ser de tipo int y ser mayor o igual a 0
                column: debe ser de tipo int y ser mayor o igual a 0
                cell: debe ser de tipo ini y ser mayor o igual a 0

            QUÉ SON:
                row: fila inicial de la selección
                column: columna inicial de la selección
                cell: la cantidad de celdas a seleccionar
        RETORNO:
            Un diccionario con las siguientes llaves:
                * type: La orientación de la selección
                * position: Las posiciones correspondientes a la selección
                * content-cell: La unión del contenido de las celdas seleccionadas

        EXCEPCIONES (ValueError):
            ValueError, si validate(row, column, cell) es Falso
            TableSectionError, si la selección es incorrecta, es decir, que en la tabla no es posible realizar
                        ese tipo de selección
        """
        if not self.validate(row, column, cell):
            raise ValueError(
                'Los parámetros no son válidos.'
            )
        output = {'type': self.__type[4], 'position': [], 'content-cell': ''}
        for i in range(cell):
            try:
                if row - i < 0:
                    raise TableSectionError("Limites excedido.")
                output['position'].append((row - i, column + i))
                output['content-cell'] += self.table[row - i][column + i]
            except IndexError:
                raise TableSectionError()
        return output

    def section_diagonal_y(self, row: int, column: int, cell: int) -> dict:
        """
        DESCRIPCIÓN `section_diagonal_y`:
            La selección en diagonal-y se realiza sobre la tabla con sentido al Noroeste
                Noroeste    N   Noreste
                        O   +   E
                Suroeste    S   Sureste

        PARÁMETROS (row, column, cell):
            CÓMO SON:
                row: debe ser de tipo int y ser mayor o igual a 0
                column: debe ser de tipo int y ser mayor o igual a 0
                cell: debe ser de tipo ini y ser mayor o igual a 0

            QUÉ SON:
                row: fila inicial de la selección
                column: columna inicial de la selección
                cell: la cantidad de celdas a seleccionar
        RETORNO:
            Un diccionario con las siguientes llaves:
                * type: La orientación de la selección
                * position: Las posiciones correspondientes a la selección
                * content-cell: La unión del contenido de las celdas seleccionadas

        EXCEPCIONES (ValueError):
            ValueError, si validate(row, column, cell) es Falso
            TableSectionError, si la selección es incorrecta, es decir, que en la tabla no es posible realizar
                        ese tipo de selección
        """
        if not self.validate(row, column, cell):
            raise ValueError(
                'Los parámetros no son válidos.'
            )
        output = {'type': self.__type[5], 'position': [], 'content-cell': ''}
        for i in range(cell):
            try:
                if row - i < 0 or column - i < 0:
                    raise ValueError("Limites excedidos.")
                output['position'].append((row - i, column - i))
                output['content-cell'] += self.table[row - i][column - i]
            except IndexError:
                raise TableSectionError()
        return output

    def section_diagonal_xr(self, row: int, column: int, cell: int) -> dict:
        """
        DESCRIPCIÓN `section_diagonal_xr`:
            La selección en diagonal-xr se realiza sobre la tabla con sentido al Suroeste
                Noroeste    N   Noreste
                        O   +   E
                Suroeste    S   Sureste

        PARÁMETROS (row, column, cell):
            CÓMO SON:
                row: debe ser de tipo int y ser mayor o igual a 0
                column: debe ser de tipo int y ser mayor o igual a 0
                cell: debe ser de tipo ini y ser mayor o igual a 0

            QUÉ SON:
                row: fila inicial de la selección
                column: columna inicial de la selección
                cell: la cantidad de celdas a seleccionar
        RETORNO:
            Un diccionario con las siguientes llaves:
                * type: La orientación de la selección
                * position: Las posiciones correspondientes a la selección
                * content-cell: La unión del contenido de las celdas seleccionadas

        EXCEPCIONES (ValueError):
            ValueError, si validate(row, column, cell) es Falso
            TableSectionError, si la selección es incorrecta, es decir, que en la tabla no es posible realizar
                        ese tipo de selección
        """

        if not self.validate(row, column, cell):
            raise ValueError(
                'Los parámetros no son válidos.'
            )
        output = {'type': self.__type[6], 'position': [], 'content-cell': ''}
        for i in range(cell):
            try:
                if column - i < 0:
                    raise TableSectionError('Limites excedidos')
                output['position'].append((row + i, column - i))
                output['content-cell'] += self.table[row + i][column - i]
            except IndexError:
                raise TableSectionError()
        return output

    def section_diagonal_yr(self, row: int, column: int, cell: int) -> dict:
        """
        DESCRIPCIÓN `section_diagonal_yr`:
            La selección en diagonal-yr se realiza sobre la tabla con sentido al Sureste
                Noroeste    N   Noreste
                        O   +   E
                Suroeste    S   Sureste

        PARÁMETROS (row, column, cell):
            CÓMO SON:
                row: debe ser de tipo int y ser mayor o igual a 0
                column: debe ser de tipo int y ser mayor o igual a 0
                cell: debe ser de tipo ini y ser mayor o igual a 0

            QUÉ SON:
                row: fila inicial de la selección
                column: columna inicial de la selección
                cell: la cantidad de celdas a seleccionar
        RETORNO:
            Un diccionario con las siguientes llaves:
                * type: La orientación de la selección
                * position: Las posiciones correspondientes a la selección
                * content-cell: La unión del contenido de las celdas seleccionadas

        EXCEPCIONES (ValueError):
            ValueError, si validate(row, column, cell) es Falso
            TableSectionError, si la selección es incorrecta, es decir, que en la tabla no es posible realizar
                        ese tipo de selección
        """
        if not self.validate(row, column, cell):
            raise ValueError(
                'Los parámetros no son válidos.'
            )
        output = {'type': self.__type[7], 'position': [], 'content-cell': ''}
        for i in range(cell):
            try:
                output['position'].append((row + i, column + i))
                output['content-cell'] += self.table[row + i][column + i]
            except IndexError:
                raise TableSectionError()
        return output

    @staticmethod
    def validate(row: int, column: int, cell: int) -> bool:
        """Valida los argumentos para obtener una sección de la tabla.

            ACCIONES:

            * Comprueba que los parámetros `row`, `column` y `cell` sean números mayores o iguales a 0. Decide si son íntegros, no si la sección es válida

            :param row: fila inicial de la selección
            :type row: int
            :param column: columna inicial de la selección
            :type column: int
            :param cell: cantidad de celdas para seleccionar
            :type cell: int
            :return: True si row, column y cell son válidos, False si uno o más de los parámetros es inválido
            :rtype: bool
        """
        return not any([not (isinstance(value, int) and value >= 0) for value in (row, column, cell)])

    def section(self, direction, row_start, column_start, cell):
        """Obtiene un sección de la tabla en cualquier dirección."""

        if direction.upper() == self.__type[0]:
            return self.section_up(row_start, column_start, cell)

        elif direction.upper() == self.__type[1]:
            return self.section_down(row_start, column_start, cell)

        elif direction.upper() == self.__type[2]:
            return self.section_right(row_start, column_start, cell)

        elif direction.upper() == self.__type[3]:
            return self.section_left(row_start, column_start, cell)

        elif direction.upper() == self.__type[4]:
            return self.section_diagonal_x(row_start, column_start, cell)

        elif direction.upper() == self.__type[5]:
            return self.section_diagonal_y(row_start, column_start, cell)

        elif direction.upper() == self.__type[6]:
            return self.section_diagonal_xr(row_start, column_start, cell)

        elif direction.upper() == self.__type[7]:
            return self.section_diagonal_yr(row_start, column_start, cell)

    def get_row(self, row: int) -> list:
        """Obtiene una fila de la tabla
        Devuelve None si no existe la fila
        """
        # si es numero mayor o igual que 0 y menor o igual que la cantidad de filas de la tabla
        if isinstance(row, int) and 0 <= row <= len(self.table):
            return self.table[row]
        else:
            return None

    def get_column(self, column: int) -> list:
        """Obtiene una column de la tabla
        Devuelve None si no existe la columna
        """
        if isinstance(column, int) and column >= 0 and len(self.table[0]):
            try:
                return list(self.section_down(0, column, len(self.table))['content-cell'])
            except TableSectionError:
                return None
        else:
            return None


class TableSection:
    # Manipula la tabla utilizando un algoritmo distinto a Tabla, uno basado en calculo y no en iteraciones.
    def __init__(self, x, y, cells, table):
        self.__x__ = x
        self.__y__ = y
        self.__cell__ = cells
        self.__table__ = table
        self.__stop = ()
        self.__start = (x, y)

    @property
    def start(self):
        return self.__start

    @property
    def stop(self):
        # el valor de stop estara disponible despues de la primera ejecuccion del metodo next
        return self.__stop

    def gn_section_right(self):
        # formula para validar la búsqueda hacia la derecha
        # y + cell <= column - 1
        # El valor de stop estara disponible despues de la primera ejecucion del metodo next

        if self.__y__ + self.__cell__ <= len(self.__table__[0]) - 1:
            self.__stop = (self.__x__, self.__y__ + self.__cell__)
            for i in range(self.__cell__ + 1):
                yield self.__x__, self.__y__ + i

    def gn_section_down(self):
        # formula para validar la búsqueda hacia la abajo
        # x + cell <= row - 1
        if self.__x__ + self.__cell__ <= len(self.__table__) - 1:
            self.__stop = (self.__x__ + self.__cell__, self.__y__)
            for i in range(self.__cell__ + 1):
                yield self.__x__ + i, self.__y__

    def gn_section_left(self):
        # formula para validar la búsqueda hacia la izquierda
        # y + 1 - cell >= 0

        if self.__y__ + 1 - self.__cell__ >= 0:
            self.__stop = (self.__x__, self.__y__ - self.__cell__)
            for i in range(self.__cell__):
                yield self.__x__, self.__y__ - i

    def gn_section_up(self):
        # formula para validar la búsqueda hacia arriba
        # x - cell >= 0

        if self.__x__ - self.__cell__ >= 0:
            self.__stop = (self.__x__ - self.__cell__, self.__y__)
            for i in range(self.__cell__ + 1):
                yield self.__x__ - i, self.__y__

    def gn_section_diagonal_x(self):
        # formula para validar la búsqueda en diagonal-x
        # x - cell >= 0 and y + cell <= column - 1
        if self.__x__ - self.__cell__ >= 0 and self.__y__ + self.__cell__ <= len(self.__table__[0]) - 1:
            self.__stop = (self.__x__ - self.__cell__, self.__y__ + self.__cell__)
            for i in range(self.__cell__ + 1):
                yield self.__x__ - i, self.__y__ + i

    def gn_section_diagonal_y(self):
        # formula para validar la búsqueda en diagonal-y
        # x - cell >= 0 and y + 1 - cell >= 0

        if self.__x__ - self.__cell__ >= 0 and self.__y__ + 1 - self.__cell__ >= 0:
            self.__stop = (self.__x__ - self.__cell__, self.__y__ - self.__cell__)
            for i in range(self.__cell__ + 1):
                yield self.__x__ - i, self.__y__ - i

    def gn_section_diagonal_xr(self):
        # formula para validar la búsqueda en diagonal-xr
        # x + cell <= row - 1 and  y + 1 - cell >= 0

        if self.__x__ + self.__cell__ <= len(self.__table__) - 1 and self.__y__ + 1 - self.__cell__ >= 0:
            self.__stop = (self.__x__ + self.__cell__, self.__y__ - self.__cell__)
            for i in range(self.__cell__ + 1):
                yield self.__x__ + i, self.__y__ - i

    def gn_section_diagonal_yr(self):
        # formula para validar la búsqueda en diagonal-yr
        # x + cell <= row - 1 and y + cell <= column - 1
        if self.__x__ + self.__cell__ <= len(self.__table__) - 1 and self.__y__ + self.__cell__ <= len(self.__table__[0]) - 1:
            self.__stop = (self.__x__ + self.__cell__, self.__y__ + self.__cell__)
            for i in range(self.__cell__ + 1):
                yield self.__x__ + i, self.__y__ + i

xy = (1, 1)
cell = 3
t = [
    ['A', 'B', 'C', 'D', 'F', 'G'],
    ['H', 'I', 'J', 'K', 'L', 'M'],
    ['Ñ', 'O', 'P', 'Q', 'R', 'S'],
    ['T', 'V', 'X', 'Y', 'Z', '0'],
    ['1', '2', '3', '4', '5', '6']]

g = TableSection(xy[0], xy[0], cell,t)

d = g.gn_section_right()
print(next(d))
