from tabulate import tabulate
from random import randrange

TYPES = ('UP', 'DOWN', 'RIGHT', 'LEFT', 'DIAGONAL-X', 'DIAGONAL-Y', 'DIAGONAL-XR', 'DIAGONAL-YR')
UP = 'UP'
DOWN = 'DOWN'
RIGHT = 'RIGHT'
LEFT = 'LEFT'
DIAGONAL_X = 'DIAGONAL-X'
DIAGONAL_Y = 'DIAGONAL-Y'
DIAGONAL_XR = 'DIAGONAL-XR'
DIAGONAL_YR = 'DIAGONAL-YR'


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
    """Permita la creación y manipulación de tablas.

       Construye la tabla en base a los argumentos pasados.
       Hay varias formas para obtener los valores para la creación de la tabla.

    Argumentos posicionales:

    Si se pasa 1 argumento, se asume que es una tabla previamente construida. Si se pasan 2 argumentos, se asume
    que el primero es el número de filas que debe tener la tabla y el segundo es son la cantidad de columnas que
    debe tener la tabla. Si se pasan 3 argumentos, se asume que el primero es la cantidad de filas que debe
    tener la tabla, el segundo representa la cantidad de columnas y el último es el contenido que desea que
    tengan las celdas inicialmente.

    Argumentos clave-valor:
        `table`, para pasar una tabla previamente construida.
        `fill`, para pasar el contenido que desea que tengan las celdas inicialmente.
        `row`: para pasar el número de filas que debe tener la tabla.
        `column`: para pasar el número de columnas que debe tener la tabla.

    Restricciones:
        * El paso de parámetros de forma arbitraria solo se permite mediante *args o **kwargs, no se puede usar ambos
            de forma simultanea.
        * Pasando argumentos por **kwargs: la clave table omite a las demás, es decir, si se pasa table no se debe de
        pasar otros argumentos en vista de que table debe ser una tabla previamente construida. Si clave table no es
        pasada, las claves row y column pasa a ser obligatorias. La clave fill es opcional, sino se provee, se usa su
        valor por defecto que es 0.

    :raise ValueError: Si se pasa parámetros por *args y **kwargs.
    :raise KeyError: Si se omite la clave table y no se pasa la clave row y column en su sustitución.
        """

    def __init__(self, *args, **kwargs):
        self.__row = 0
        self.__column = 0
        self.__fill = 0
        self.__type = TYPES
        self.__table = None
        self.__make(*args, **kwargs)

    def __make(self, *args, **kwargs):
        if args and kwargs:
            raise ValueError('No se permite el paso de parámetros por *args y **kwargs de forma simultanea.')

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
                raise ValueError(f'se esperaban 3, 2 o 1 argumentos y pasaron {len(args)}: {args} ')

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
        return tabulate(self.__table, tablefmt="grid")

    def __repr__(self):
        return f"{self.__class__.__name__}({self.row}, {self.column}, {self.fill})"

    # Documentado
    def dimension(self) -> str:
        """Devuelve la dimensiones de la tabla.

        :return: Retorna la dimensión de la tabla filas por columnas.
        :rtype str
        """
        return f"{self.row}x{self.column}"

    # Documentado
    @property
    def row(self) -> int:
        """Devuelve el número de filas de la tabla."""
        return self.__row

    # Documentado
    @property
    def column(self) -> int:
        """Devuelve el número de columnas de la tabla."""
        return self.__column

    # Documentado
    @property
    def fill(self):
        """Devuelve el tipo de llenado que tiene la tabla.
        :return: Devuelve None cuando la tabla es pasada ya construida, debido a que estas pueden tener un contenido
        arbitrario.
        """
        return self.__fill

    # Documentado
    @property
    def table(self) -> list[[list, ..., list]]:
        """Devuelve la tabla."""
        return self.__table

    # Documentado
    @table.setter
    def table(self, value) -> None:
        """Establece una tabla previamente construida.
        La tabla previamente construida debe cumplir las siguientes directivas:

        * La tabla debe ser de tipo lista y todos sus elementos también
        * Las dimensiones mínimas admitidas son 1x1
        * El número de celdas en cada fila debe ser igual.

        :param list value: Es una matriz previamente construida.
        :raise TableStructureError:  Si la matriz pasada no cumple con las directivas.
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

    # Documentado
    @row.setter
    def row(self, value):
        """Actualiza el número de filas de la tabla.
        :param int value: Nuevo número de filas de la tabla.
        :raise ValueError: Si value no es de tipo int y mayor que 0
        """
        if isinstance(value, int) and value > 0:
            self.__row = value
            self.__table = [[self.fill] * self.column for _ in range(self.row)]
        else:
            raise ValueError("row debe ser un numero y deber mayor que 0")

    # Documentado
    @column.setter
    def column(self, value):
        """Actualiza el número de columnas de la tabla.

        :param int value: Nueva número de columnas de la tabla.

        :raise ValueError: Si value no es de tipo int y mayor que 0.
        """
        if isinstance(value, int) and value > 0:
            self.__column = value
            self.__table = [[self.fill] * self.column for _ in range(self.row)]
        else:
            raise ValueError("column debe ser un número y debe ser mayor que 0")

    # Documentado
    def section_up(self, row: int, column: int, cell: int) -> dict:
        """Permite realizar un selección sobre la tabla en sentido N (hacia arriba),
        partiendo del punto (`row`, `column`), abarcando un rango `cell`.
            NO  N   NE
            O   +   E
            SO  S  SE

        :param int row: Fila inicial de la selección. Debe ser mayor o igual a 0.
        :param int column: Columna inicial de la selección. Debe ser mayor o igual a 0.
        :param int cell: Cantidad de celdas de la tabla a seleccionar. Debe ser mayor o igual a 0.

        :return: Diccionario que contiene información de la selección. Específicamente el tipo de selección,
                la posición y el contenido de las celdas de las posiciones seleccionadas.
                Un diccionario con las siguientes llaves:
                * type: La orientación de la selección
                * position: Las posiciones correspondientes a la selección
        :rtype: dict

        :raise ValueError: si self.validate(row, column, cell) retorna Falso

        :raise TableSectionError: si la selección es incorrecta, es decir, que en la tabla no es
         posible realizar ese tipo de selección.
        """
        if not self.validate(row, column, cell):
            raise ValueError(
                'Los parámetros no son válidos.'
            )
        output = {'type': self.__type[0], 'position': []}
        for i in range(cell):
            if 0 > row - i:
                raise TableSectionError()
            output['position'].append((row - i, column))
            # output['content-cell'] += self.table[row - i][column]
        return output

    # Documentado
    def section_down(self, row: int, column: int, cell: int) -> dict:
        """Permite realizar un selección sobre la tabla en sentido S (hacia abajo),
        partiendo del punto (`row`, `column`), abarcando un rango `cell`.
            NO  N   NE
            O   +   E
            SO  S  SE

        :param int row: Fila inicial de la selección. Debe ser mayor o igual a 0.
        :param int column: Columna inicial de la selección. Debe ser mayor o igual a 0.
        :param int cell: Cantidad de celdas de la tabla a seleccionar. Debe ser mayor o igual a 0.


        :return: Diccionario que contiene información de la selección. Específicamente el tipo de selección,
                la posición y el contenido de las celdas de las posiciones seleccionadas.
                Un diccionario con las siguientes llaves:
                * type: La orientación de la selección
                * position: Las posiciones correspondientes a la selección
        :rtype: dict

        :raise ValueError: si self.validate(row, column, cell) retorna Falso

        :raise TableSectionError: si la selección es incorrecta, es decir, que en la tabla no es
         posible realizar ese tipo de selección.
        """

        if not self.validate(row, column, cell):
            raise ValueError(
                'Los parámetros no son válidos.'
            )
        output = {'type': self.__type[1], 'position': []}
        for i in range(cell):
            try:
                output['position'].append((row + i, column))
                # output['content-cell'] += self.table[row + i][column]
            except IndexError:
                raise TableSectionError("Limites excedidos.")
        return output

    # Documentado
    def section_right(self, row: int, column: int, cell: int) -> dict:
        """Permite realizar un selección sobre la tabla en sentido E (hacia la derecha),
        partiendo del punto (`row`, `column`), abarcando un rango `cell`.
            NO  N   NE
            O   +   E
            SO  S  SE

        :param int row: Fila inicial de la selección. Debe ser mayor o igual a 0.
        :param int column: Columna inicial de la selección. Debe ser mayor o igual a 0.
        :param int cell: Cantidad de celdas de la tabla a seleccionar. Debe ser mayor o igual a 0.


        :return: Diccionario que contiene información de la selección. Específicamente el tipo de selección,
                la posición y el contenido de las celdas de las posiciones seleccionadas.
                Un diccionario con las siguientes llaves:
                * type: La orientación de la selección
                * position: Las posiciones correspondientes a la selección
        :rtype: dict

        :raise ValueError: si self.validate(row, column, cell) retorna Falso

        :raise TableSectionError: si la selección es incorrecta, es decir, que en la tabla no es
         posible realizar ese tipo de selección.
        """
        if not self.validate(row, column, cell):
            raise ValueError(
                'Los parámetros no son válidos.'
            )
        output = {'type': self.__type[2], 'position': []}
        for i in range(cell):
            try:
                output['position'].append((row, column + i))
                # output['content-cell'] += self.table[row][column + i]
            except IndexError:
                raise TableSectionError()
        return output

    # Documentado
    def section_left(self, row: int, column: int, cell: int) -> dict:
        """Permite realizar un selección sobre la tabla en sentido O (hacia la izquierda),
        partiendo del punto (`row`, `column`), abarcando un rango `cell`.
            NO  N   NE
            O   +   E
            SO  S  SE

        :param int row: Fila inicial de la selección. Debe ser mayor o igual a 0.
        :param int column: Columna inicial de la selección. Debe ser mayor o igual a 0.
        :param int cell: Cantidad de celdas de la tabla a seleccionar. Debe ser mayor o igual a 0.


        :return: Diccionario que contiene información de la selección. Específicamente el tipo de selección,
                la posición y el contenido de las celdas de las posiciones seleccionadas.
                Un diccionario con las siguientes llaves:
                * type: La orientación de la selección
                * position: Las posiciones correspondientes a la selección
        :rtype: dict

        :raise ValueError: si self.validate(row, column, cell) retorna Falso

        :raise TableSectionError: si la selección es incorrecta, es decir, que en la tabla no es
         posible realizar ese tipo de selección.
        """
        if not self.validate(row, column, cell):
            raise ValueError(
                'Los parámetros no son válidos.'
            )
        output = {'type': self.__type[3], 'position': []}
        for i in range(cell):
            if column - i < 0:
                raise TableSectionError()
            output['position'].append((row, column - i))
            # output['content-cell'] += self.table[row][column - i]
        return output

    # Documentado
    def section_diagonal_x(self, row: int, column: int, cell: int) -> dict:
        """Permite realizar un selección sobre la tabla en sentido NE (hacia la derecha y hacia arriba),
        partiendo del punto (`row`, `column`), abarcando un rango `cell`.
            NO  N   NE
            O   +   E
            SO  S  SE

        :param int row: Fila inicial de la selección. Debe ser mayor o igual a 0.
        :param int column: Columna inicial de la selección. Debe ser mayor o igual a 0.
        :param int cell: Cantidad de celdas de la tabla a seleccionar. Debe ser mayor o igual a 0.


        :return: Diccionario que contiene información de la selección. Específicamente el tipo de selección,
                la posición y el contenido de las celdas de las posiciones seleccionadas.
                Un diccionario con las siguientes llaves:
                * type: La orientación de la selección
                * position: Las posiciones correspondientes a la selección
        :rtype: dict

        :raise ValueError: si self.validate(row, column, cell) retorna Falso

        :raise TableSectionError: si la selección es incorrecta, es decir, que en la tabla no es
         posible realizar ese tipo de selección.
        """
        if not self.validate(row, column, cell):
            raise ValueError(
                'Los parámetros no son válidos.'
            )
        output = {'type': self.__type[4], 'position': []}
        for i in range(cell):
            try:
                if row - i < 0:
                    raise TableSectionError("Limites excedido.")
                output['position'].append((row - i, column + i))
                # output['content-cell'] += self.table[row - i][column + i]
            except IndexError:
                raise TableSectionError()
        return output

    # Documentado
    def section_diagonal_y(self, row: int, column: int, cell: int) -> dict:
        """Permite realizar un selección sobre la tabla en sentido NO (hacia la izquierda y hacia arriba),
        partiendo del punto (`row`, `column`), un rango `cell`.
            NO  N   NE
            O   +   E
            SO  S  SE

        :param int row: Fila inicial de la selección. Debe ser mayor o igual a 0.
        :param int column: Columna inicial de la selección. Debe ser mayor o igual a 0.
        :param int cell: Cantidad de celdas de la tabla a seleccionar. Debe ser mayor o igual a 0.


        :return: Diccionario que contiene información de la selección. Específicamente el tipo de selección,
                la posición y el contenido de las celdas de las posiciones seleccionadas.
                Un diccionario con las siguientes llaves:
                * type: La orientación de la selección
                * position: Las posiciones correspondientes a la selección
        :rtype: dict

        :raise ValueError: si self.validate(row, column, cell) retorna Falso

        :raise TableSectionError: si la selección es incorrecta, es decir, que en la tabla no es
         posible realizar ese tipo de selección.
        """
        if not self.validate(row, column, cell):
            raise ValueError(
                'Los parámetros no son válidos.'
            )
        output = {'type': self.__type[5], 'position': []}
        for i in range(cell):
            try:
                if row - i < 0 or column - i < 0:
                    raise ValueError("Limites excedidos.")
                output['position'].append((row - i, column - i))
                # output['content-cell'] += self.table[row - i][column - i]
            except IndexError:
                raise TableSectionError()
        return output

    # Documentado
    def section_diagonal_xr(self, row: int, column: int, cell: int) -> dict:
        """Permite realizar un selección sobre la tabla en sentido SO (hacia abajo y hacia la izquierda),
        partiendo del punto (`row`, `column`), abarcando un rango `cell`.
            NO  N   NE
            O   +   E
            SO  S  SE

        :param int row: Fila inicial de la selección. Debe ser mayor o igual a 0.
        :param int column: Columna inicial de la selección. Debe ser mayor o igual a 0.
        :param int cell: Cantidad de celdas de la tabla a seleccionar. Debe ser mayor o igual a 0.


        :return: Diccionario que contiene información de la selección. Específicamente el tipo de selección,
                la posición y el contenido de las celdas de las posiciones seleccionadas.
                Un diccionario con las siguientes llaves:
                * type: La orientación de la selección
                * position: Las posiciones correspondientes a la selección
        :rtype: dict

        :raise ValueError: si self.validate(row, column, cell) retorna Falso

        :raise TableSectionError: si la selección es incorrecta, es decir, que en la tabla no es
         posible realizar ese tipo de selección.
        """

        if not self.validate(row, column, cell):
            raise ValueError(
                'Los parámetros no son válidos.'
            )
        output = {'type': self.__type[6], 'position': []}
        for i in range(cell):
            try:
                if column - i < 0:
                    raise TableSectionError('Limites excedidos')
                output['position'].append((row + i, column - i))
                # output['content-cell'] += self.table[row + i][column - i]
            except IndexError:
                raise TableSectionError()
        return output

    # Documentado
    def section_diagonal_yr(self, row: int, column: int, cell: int) -> dict:
        """Permite realizar un selección sobre la tabla en sentido SE (hacia abajo y hacia la derecha),
        partiendo del punto (`row`, `column`), abarcando un rango `cell`.
            NO  N   NE
            O   +   E
            SO  S  SE

        :param int row: Fila inicial de la selección. Debe ser mayor o igual a 0.
        :param int column: Columna inicial de la selección. Debe ser mayor o igual a 0.
        :param int cell: Cantidad de celdas de la tabla a seleccionar. Debe ser mayor o igual a 0.


        :return: Diccionario que contiene información de la selección. Específicamente el tipo de selección,
                la posición y el contenido de las celdas de las posiciones seleccionadas.
                Un diccionario con las siguientes llaves:
                * type: La orientación de la selección
                * position: Las posiciones correspondientes a la selección
        :rtype: dict

        :raise ValueError: si self.validate(row, column, cell) retorna Falso

        :raise TableSectionError: si la selección es incorrecta, es decir, que en la tabla no es
         posible realizar ese tipo de selección.
        """
        if not self.validate(row, column, cell):
            raise ValueError(
                'Los parámetros no son válidos.'
            )
        output = {'type': self.__type[7], 'position': []}
        for i in range(cell):
            try:
                output['position'].append((row + i, column + i))
                # output['content-cell'] += self.table[row + i][column + i]
            except IndexError:
                raise TableSectionError()
        return output

    # Documentado
    @staticmethod
    def validate(row: int, column: int, cell: int) -> bool:
        """Método estático que valida los argumentos para obtener una sección de la tabla.

            Comprueba que los parámetros `row`, `column` y `cell` sean números mayores o iguales a 0.
            Decide si son íntegros, no si la selección es válida.

            :param int row: fila inicial de la selección.
            :param int column: columna inicial de la selección.
            :param int cell: cantidad de celdas para seleccionar.
            :return: True si row, column y cell son válidos, False si uno o más de los parámetros es inválido.
            :rtype: bool
        """
        return not any([not (isinstance(value, int) and value >= 0) for value in (row, column, cell)])

    # Documentado
    def section(self, direction: str, row_start, column_start, cell) -> dict:
        """Obtiene un sección de la tabla en cualquier dirección.
        Combina los métodos de selección de la tabla.

        :param str direction:
        Dirección de la selección. 'UP', paso los parámetros `row_start`, `column_start`
        y `cell` al método section_up; 'DOWN', paso los parámetros `row_start`, `column_start`
        y `cell` al método section_down; 'RIGHT', paso los parámetros `row_start`, `column_start`
        y `cell` al método section_right; 'LEFT', paso los parámetros `row_start`, `column_start`
        y `cell` al método section_left; 'DIAGONAL-X', paso los parámetros `row_start`, `column_start`
        y `cell` al método section_diagonal_x; 'DIAGONAL-Y', paso los parámetros `row_start`, `column_start`
        y `cell` al método section_diagonal_y; 'DIAGONAL-XR', paso los parámetros `row_start`, `column_start`
        y `cell` al método section_diagonal_xr; 'DIAGONAL-YR', paso los parámetros `row_start`, `column_start`
        y `cell` al método section_diagonal_yr.

        :param int row_start: Fila inicial de la selección. Debe ser mayor o igual a 0.
        :param int column_start: Columna inicial de la selección. Debe ser mayor o igual a 0.
        :param int cell: Cantidad de celdas de la tabla a seleccionar. Debe ser mayor o igual a 0.

        :return: Diccionario que contiene información de la selección. Específicamente el tipo de selección,
                la posición y el contenido de las celdas de las posiciones seleccionadas.
                Un diccionario con las siguientes llaves:
                * type: La orientación de la selección
                * position: Las posiciones correspondientes a la selección
                * content-cell: La unión del contenido de las celdas seleccionadas
        :rtype: dict

        :raise ValueError: si self.validate(row, column, cell) retorna Falso

        :raise TableSectionError: si la selección es incorrecta, es decir, que en la tabla no es
         posible realizar ese tipo de selección.
        """

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

    # Documentado
    def get_row(self, row: int) -> list:
        """Obtiene una fila completa de la tabla.

        :param int row: fila a obtener.

        :return: Retorna una lista que representa la fila obtenida. Retorna `None` si la fila no existe
        :rtype: list
        """
        # si es numero mayor o igual que 0 y menor o igual que la cantidad de filas de la tabla
        if isinstance(row, int) and 0 <= row <= len(self.table):
            return self.table[row]

    # Documentado
    def get_column(self, column: int) -> list:
        """Obtiene una columna completa de la tabla.

            :param int column: columna a obtener.

            :return: Retorna una lista que representa la columna obtenida. Retorna `None` si la columna no existe
            :rtype: list
            """
        if isinstance(column, int) and column >= 0 and len(self.table[0]):
            try:
                return [self.table[x[0]][x[1]] for x in self.section_down(0, column, len(self.table))['position']]
            except TableSectionError:
                pass


class TableSection:
    """Selecciona partes de la tabla utilizando un algoritmo basado en cálculos de inecuaciones y no en iteraciones."""

    def __init__(self, x, y, cells, table):
        """
        :param int x: Representa la fila inicial de la selección.
        :param int y: Representa la columna inicial de la selección.
        :param int cells: Representa la cantidad de celdas a seleccionar de la tabla
        :param list[list, ..., list] table: Es la tabla sobre la cual se realizarán las operaciones de selección.
        """
        self.__x__ = x
        self.__y__ = y
        self.__cell__ = cells
        self.__table__ = table
        self.__stop = ()
        self.__start = (x, y)

    # Documentado
    @property
    def start(self) -> tuple:
        """Representa la posición inicial de la selección.
        :return: Es un par ordenado (x, y) que representa la posición inicial de la selección.
        :rtype: tuple
        """
        return self.__start

    # Documentado
    @property
    def stop(self) -> tuple:
        """Representa la posición final de la selección.
        NOTA: el valor de stop estará disponible justo después de la primera ejecución del método next sobre el
        generador retornado por cualquiera de los métodos de selección de la tabla. Antes de la primero ejecución del
        método next sobre cualquiera de los generadores retornados por alguno de los métodos de selección de la tabla,
        stop será igual a ()
        :return: Devuelva una par ordenado (x, y) que son la última celda seleccionada.
        :rtype: tuple
        """
        return self.__stop

    # Documentado
    def gn_section_right(self):
        """Permite obtener una selección en sentido E (hacia la derecha).
        La selección inicia en (self.x, self.y) abarcando un rango de celdas indicado por self.cells sobre self.table
        en dirección E.
            NO  N   NE
            O   +   E
            SO  S  SE
        :return: Un generador que contiene las posiciones seleccionadas de la tabla. retorna None si la selección
        no se puede realizar.
        :rtype: generator
        """
        # formula para validar la búsqueda hacia la derecha
        # y + cell <= column - 1
        if self.__y__ + self.__cell__ <= len(self.__table__[0]) - 1:
            self.__stop = (self.__x__, self.__y__ + self.__cell__)
            for i in range(self.__cell__ + 1):
                yield self.__x__, self.__y__ + i

    # Documentado
    def gn_section_down(self):
        """Permite obtener una selección en sentido S (hacia abajo).
        La selección inicia en (self.x, self.y) abarcando un rango de celdas indicado por self.cells sobre self.table
        en dirección S.
            NO  N   NE
            O   +   E
            SO  S  SE
        :return: Un generador que contiene las posiciones seleccionadas de la tabla. retorna None si la selección
        no se puede realizar.
        :rtype: generator
        """
        # formula para validar la búsqueda hacia la abajo
        # x + cell <= row - 1
        if self.__x__ + self.__cell__ <= len(self.__table__) - 1:
            self.__stop = (self.__x__ + self.__cell__, self.__y__)
            for i in range(self.__cell__ + 1):
                yield self.__x__ + i, self.__y__

    # Documentado
    def gn_section_left(self):
        """Permite obtener una selección en sentido O (hacia la izquierda).
        La selección inicia en (self.x, self.y) abarcando un rango de celdas indicado por self.cells sobre self.table
        en dirección O.
            NO  N   NE
            O   +   E
            SO  S  SE
        :return: Un generador que contiene las posiciones seleccionadas de la tabla. retorna None si la selección
        no se puede realizar.
        :rtype: generator
        """
        # formula para validar la búsqueda hacia la izquierda
        # y + 1 - cell >= 0

        if self.__y__ + 1 - self.__cell__ >= 0:
            self.__stop = (self.__x__, self.__y__ - self.__cell__)
            for i in range(self.__cell__):
                yield self.__x__, self.__y__ - i

    # Documentado
    def gn_section_up(self):
        """Permite obtener una selección en sentido N (hacia arriba).
        La selección inicia en (self.x, self.y) abarcando un rango de celdas indicado por self.cells sobre self.table
        en dirección N.
            NO  N   NE
            O   +   E
            SO  S  SE
        :return: Un generador que contiene las posiciones seleccionadas de la tabla. retorna None si la selección
        no se puede realizar.
        :rtype: generator
        """
        # formula para validar la búsqueda hacia arriba
        # x - cell >= 0

        if self.__x__ - self.__cell__ >= 0:
            self.__stop = (self.__x__ - self.__cell__, self.__y__)
            for i in range(self.__cell__ + 1):
                yield self.__x__ - i, self.__y__

    # Documentado
    def gn_section_diagonal_x(self):
        """Permite obtener una selección en sentido NE (hacia la derecha y hacia arriba).
        La selección inicia en (self.x, self.y) abarcando un rango de celdas indicado por self.cells sobre self.table
        en dirección NE.
            NO  N   NE
            O   +   E
            SO  S  SE
        :return: Un generador que contiene las posiciones seleccionadas de la tabla. retorna None si la selección
        no se puede realizar.
        :rtype: generator
        """
        # formula para validar la búsqueda en diagonal-x
        # x - cell >= 0 and y + cell <= column - 1
        if self.__x__ - self.__cell__ >= 0 and self.__y__ + self.__cell__ <= len(self.__table__[0]) - 1:
            self.__stop = (self.__x__ - self.__cell__, self.__y__ + self.__cell__)
            for i in range(self.__cell__ + 1):
                yield self.__x__ - i, self.__y__ + i

    # Documentado
    def gn_section_diagonal_y(self):
        """Permite obtener una selección en sentido NO (hacia la izquierda y hacia arriba).
        La selección inicia en (self.x, self.y) abarcando un rango de celdas indicado por self.cells sobre self.table
        en dirección NO.
            NO  N   NE
            O   +   E
            SO  S  SE
        :return: Un generador que contiene las posiciones seleccionadas de la tabla. retorna None si la selección
        no se puede realizar.
        :rtype: generator
        """
        # formula para validar la búsqueda en diagonal-y
        # x - cell >= 0 and y + 1 - cell >= 0

        if self.__x__ - self.__cell__ >= 0 and self.__y__ + 1 - self.__cell__ >= 0:
            self.__stop = (self.__x__ - self.__cell__, self.__y__ - self.__cell__)
            for i in range(self.__cell__ + 1):
                yield self.__x__ - i, self.__y__ - i

    # Documentado
    def gn_section_diagonal_xr(self):
        """Permite obtener una selección en sentido SO (hacia la izquierda y hacia abajo).
        La selección inicia en (self.x, self.y) abarcando un rango de celdas indicado por self.cells sobre self.table
        en dirección SO.
            NO  N   NE
            O   +   E
            SO  S  SE
        :return: Un generador que contiene las posiciones seleccionadas de la tabla. retorna None si la selección
        no se puede realizar.
        :rtype: generator
        """
        # formula para validar la búsqueda en diagonal-xr
        # x + cell <= row - 1 and  y + 1 - cell >= 0

        if self.__x__ + self.__cell__ <= len(self.__table__) - 1 and self.__y__ + 1 - self.__cell__ >= 0:
            self.__stop = (self.__x__ + self.__cell__, self.__y__ - self.__cell__)
            for i in range(self.__cell__ + 1):
                yield self.__x__ + i, self.__y__ - i

    # Documentado
    def gn_section_diagonal_yr(self):
        """Permite obtener una selección en sentido SE (hacia la derecha y hacia abajo).
        La selección inicia en (self.x, self.y) abarcando un rango de celdas indicado por self.cells sobre self.table
        en dirección SE.
            NO  N   NE
            O   +   E
            SO  S  SE
        :return: Un generador que contiene las posiciones seleccionadas de la tabla. retorna None si la selección
        no se puede realizar.
        :rtype: generator
        """
        # formula para validar la búsqueda en diagonal-yr
        # x + cell <= row - 1 and y + cell <= column - 1
        if self.__x__ + self.__cell__ <= len(self.__table__) - 1 and self.__y__ + self.__cell__ <= len(
                self.__table__[0]) - 1:
            self.__stop = (self.__x__ + self.__cell__, self.__y__ + self.__cell__)
            for i in range(self.__cell__ + 1):
                yield self.__x__ + i, self.__y__ + i


def create_table(row: int,
                 column: int,
                 fill: int = 0,
                 random_fill: bool = False,
                 _min: int = 0,
                 _max: int = 100,
                 exclude=None):
    """Crea una tabla de con dimensiones y contenido personalizado

    :param int row: Cantidad de filas que debe tener la tabla.
    :param int column: Cantidad de columnas que debe tener la tabla.
    :param int fill: Contenido de las celdas de la tabla. Si se random_fill igual a True, el valor de fill es ignorado.
    :param int random_fill: Si es igual a True, se llenarán las celdas con números aleatorios entre _min y _max.
    :param int _min: Mínimo número con el que se llenará la tabla.
    :param int _max: Máximo número con el que se llenará la tabla.
    :param list exclude: Lista de números que desea excluir de las celdas de la tabla.
    Solo funciona si se usa random_fill.
    :return: Retorna una tabla generada con los parámetros establecidos.
    :rtype: list
    """

    if random_fill:
        output = []
        for r in range(row):
            col = []
            for c in range(column):
                if exclude is not None:
                    number = randrange(_min, _max)
                    while number in exclude:
                        number = randrange(_min, _max)
                    col.append(number)
                else:
                    number = randrange(_min, _max)
                    col.append(number)
            output.append(col)
        return output
    else:
        return [[fill] * column for _ in range(row)]

# Tabla creada automáticamente
# t = create_table(3, 5, random_fill=True, _min=1, _max=50)

# t = [
#     [7, 30, 36, 16, 7, 43, 8, 47, 9, 20, 27, 4],
#     [1, 9, 2, 21, 42, 5, 13, 6, 47, 31, 34, 11],
#     [39, 39, 38, 15, 21, 23, 8, 4, 39, 2, 1, 7],
#     [7, 16, 34, 4, 4, 27, 1, 41, 9, 24, 45, 29],
#     [32, 36, 8, 38, 45, 10, 16, 6, 47, 1, 3, 2],
#     [1, 1, 45, 16, 37, 4, 11, 40, 27, 25, 8, 2],
#     [5, 31, 1, 49, 3, 17, 22, 4, 14, 19, 11, 2]
# ]
#
# k = Table(t)
# print(k.section_diagonal_yr(0, 0, 5))

# t = [
#     [7, 30, 36, 16, 7, 43, 8, 47, 9, 20, 27, 4],
#     [1, 9, 2, 21, 42, 5, 13, 6, 47, 31, 34, 11],
#     [39, 39, 38, 15, 21, 23, 8, 4, 39, 2, 1, 7],
#     [7, 16, 34, 4, 4, 27, 1, 41, 9, 24, 45, 29],
#     [32, 36, 8, 38, 45, 10, 16, 6, 47, 1, 3, 2],
#     [1, 1, 45, 16, 37, 4, 11, 40, 27, 25, 8, 2],
#     [5, 31, 1, 49, 3, 17, 22, 4, 14, 19, 11, 2]
# ]
#
# k = Table(t)
# print(k.section_diagonal_yr(0, 0, 5))


