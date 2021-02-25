import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):

    def __init__(self, life: GameOfLife, cell_size: int=10, speed: int=10) -> None:
        super().__init__(life)
        self.cell_size=cell_size
        self.speed=speed
        # Высота и ширина окна
        self.width = self.life.cols*cell_size
        self.height = self.life.rows*cell_size
        # Устанавливаем размер окна
        self.screen_size =self.width, self.height
        # Создание окна
        self.screen = pygame.display.set_mode(self.screen_size)
        # Скорость игры
        self.speed = speed


    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (0, y), (self.width, y))

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for i,line in enumerate(self.life.curr_generation):
            for j,cell in enumerate(line):
                color = pygame.Color('white')
                if cell: color=pygame.Color('green')
                pygame.draw.rect(self.screen, color, (j*self.cell_size, i*self.cell_size,self.cell_size,self.cell_size))


    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        running = True
        paused = False
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            # Реализация паузы по нажатии на пробел
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        paused = not paused
                        self.draw_grid()
                        self.draw_lines()
                        pygame.display.flip()
            # Возможность изменить состояние клетки во время игры
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button in [1,3]:
                        x,y=pygame.mouse.get_pos()
                        cell_pos=(x//self.cell_size, y//self.cell_size)
                        self.life.curr_generation[cell_pos[1]][cell_pos[0]] = abs(self.life.curr_generation[cell_pos[1]][cell_pos[0]] - 1)
                        self.draw_grid()
                        self.draw_lines()
                        pygame.display.flip()
            if not paused:
                # Отрисовка списка клеток
                # Выполнение одного шага игры (обновление состояния ячеек)
                self.draw_grid()
                self.draw_lines()
                self.life.step()
                pygame.display.flip()
            #    if self.life.is_max_generations_exceeded or not self.life.is_changing:
            #        break
                clock.tick(self.speed)
        pygame.quit()


if __name__ == "__main__":
    cols=int(input('cols\n'))
    rows=int(input('rows\n'))
    max_gens=int(input('maximum generations or \'0\' for infinity\n'))
    if max_gens == 0:
        life=GameOfLife(size=(rows,cols))
    else:
        life=GameOfLife(size=(rows,cols), max_generations=max_gens)
    cell_size=int(input('cell_size\n'))
    speed=int(input('speed\n'))
    gui=GUI(life=life,cell_size=cell_size,speed=speed)
    gui.run()
