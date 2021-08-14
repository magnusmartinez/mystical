# Mystical
Manipulación de tablas de forma abstracta y sistematizada, permitiendo la selección en cualquier 
dirección de una tabla.

## Instalación
Para realizar la instalación de _Mystical_, mediante el uso de pip deberás ejecutar dentro de tu terminal el siguiente
comando: `pip install mystical`.


## Uso

### Importamos Mystical
```python
# Importamos la librería
from mystical import table
```

Declaramos la tabla sobre la que queremos trabajar o usamos la función `create_table`
para crearla:
```python
# Construimos la tabla manualmente 7x12
t = [
        [7, 30, 36, 16, 7, 43, 8, 47, 9, 20, 27, 4],
        [1, 9, 2, 21, 42, 5, 13, 6, 47, 31, 34, 11],
        [39, 39, 38, 15, 21, 23, 8, 4, 39, 2, 1, 7],
        [7, 16, 34, 4, 4, 27, 1, 41, 9, 24, 45, 29],
        [32, 36, 8, 38, 45, 10, 16, 6, 47, 1, 3, 2],
        [1, 1, 45, 16, 37, 4, 11, 40, 27, 25, 8, 2],
        [5, 31, 1, 49, 3, 17, 22, 4, 14, 19, 11, 2]
]
```
Imaginemos que necesitamos obtener ciertas celdas de esa tabla, ejemplo, 5 celdas partiendo desde el punto (0, 0) en dirección 
Sureste (SE):
```
NO  N  NE
O   +   E
SO  S  SE
```
Entonces, para esta dirección de selección debemos usar el método `section_diagonal_yr` de la clase `Table`:
```python
my_table = table.Table(t)
selection = my_table.section_diagonal_yr()
print(selection)  # {'type': 'DIAGONAL-YR', 'position': [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]}

```
En ejemplo completo sería:
```python
# Importamos la librería
from mystical import table

# Construimos la tabla manualmente 7x12
t = [
        [7, 30, 36, 16, 7, 43, 8, 47, 9, 20, 27, 4],
        [1, 9, 2, 21, 42, 5, 13, 6, 47, 31, 34, 11],
        [39, 39, 38, 15, 21, 23, 8, 4, 39, 2, 1, 7],
        [7, 16, 34, 4, 4, 27, 1, 41, 9, 24, 45, 29],
        [32, 36, 8, 38, 45, 10, 16, 6, 47, 1, 3, 2],
        [1, 1, 45, 16, 37, 4, 11, 40, 27, 25, 8, 2],
        [5, 31, 1, 49, 3, 17, 22, 4, 14, 19, 11, 2]
]
my_table = table.Table(t)
selection = my_table.section_diagonal_yr()
print(selection) 
# {'type': 'DIAGONAL-YR', 'position': [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]}
```

Todos los métodos de selección devuelve un diccionario con dos claves, type, 
que representa el tipo de búsqueda realizada;
position, que es una lista con las posiciones de las celdas que se encuentran dentro del rango de selección.

```
{
    'type': 'DIAGONAL-YR',
    'position': [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
}
```
