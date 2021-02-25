import pathlib
import random

from typing import List, Optional, Tuple


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(
        self,
        size: Tuple[int, int],
        randomize: bool=True,
        max_generations: Optional[float]=float('inf')
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool=False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cols` х `rows`.
        """
        grid=[[0]*self.cols for i in range(self.rows)]
        if randomize:
            for i in range(self.rows):
                for j in range(self.cols):
                    grid[i][j] = random.choice([0,1])
        return grid


    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        x,y=cell
        cells=[]
        if y-1 >= 0:
            cells.append((x,y-1))
            if x+1<self.cols:
                cells.append((x+1,y-1))
        if x+1<self.cols:
            cells.append((x+1,y))
            if y+1<self.rows:
                cells.append((x+1,y+1))
        if y+1<self.rows:
            cells.append((x,y+1))
            if x-1>=0:
                cells.append((x-1,y+1))
        if x-1>=0:
            cells.append((x-1,y))
            if y-1>=0:
                cells.append((x-1,y-1))
        return cells

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        newgrid=[[0]*self.cols for i in range(self.rows)]
        for i,line in enumerate(self.prev_generation):
            for j,this in enumerate(line):
                cell=(j,i)
                neighbours_count=sum([self.prev_generation[c[1]][c[0]] for c in self.get_neighbours(cell)])
                if self.prev_generation[i][j] == 1:
                    if neighbours_count in [2,3]:
                        newgrid[i][j]=1
                    else:
                        newgrid[i][j]=0
                else:
                    if neighbours_count==3:
                        newgrid[i][j]=1
                    else:
                        newgrid[i][j]=0
        return newgrid
    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation=self.curr_generation
        self.curr_generation=self.get_next_generation()
        self.generations+=1


    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        is_exceeded=False
        if self.generations>self.max_generations:
            is_exceeded=True
        return is_exceeded

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        is_changing=False
        for i in range(self.rows):
            if self.prev_generation[i]!=self.curr_generation[i]:
                is_changing=True
        return is_changing

    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """
        grid=[]
        file=open(filename,'r')
        for i,line in enumerate(file):
            grid.append([])
            for c in line[:-1]:
                grid[i].append(int(c))
        game_from_file=GameOfLife(size=(len(grid),len(grid[0])), randomize=False)
        game_from_file.curr_generation=grid
        return game_from_file

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        file=open(filename,'w')
        for i in self.curr_generation:
            for c in i:
                file.write(str(c))
            file.write('\n')
