#Консольная реализация
#Импорт библиотек--------------------------------------------------------------
import curses
import argparse
import time

#Импорт модулей
from life import GameOfLife
from ui import UI
#------------------------------------------------------------------------------

#Реализация класса игры в жизнь в консольном интерфейсе------------------------
class Console(UI):
    ''' Класс реализующий консольный интерфейс'''
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        '''Функция для отрисовки границ поля'''
        curses.resize_term(self.life.rows + 2, self.life.cols + 2)
        screen.border('|', '|', '-', '-', '+', '+', '+', '+')

    def draw_grid(self, screen) -> None:
        '''Функция для отрисовки поля'''
        for y,line in enumerate(self.life.curr_generation):
            newline = ""
            for c in line:
                if c:
                    newline += "*"
                else:
                    newline += " "
            screen.addstr(y+1, 1, newline)

    def run(self) -> None:
        '''Запуск игры в консольном интерфейсе.
        Игра останавливается, если поле перестало изменяться
        или достигнуто максимальное число поколений'''
        while self.life.is_changing and self.life.is_max_generations_exceed:
            screen = curses.initscr()
            screen.clear()
            self.draw_borders(screen)
            self.draw_grid(screen)
            self.life.step()
            screen.refresh()
            time.sleep(0.5)
        curses.endwin()
#------------------------------------------------------------------------------

#Непосредственный запуск игры с передачей параметров---------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Реализация игры \"Жизнь\" в консольном интерфейсе.')
    parser.add_argument("--cols", default = 20, type = int, help = "Количество столбцов на поле")
    parser.add_argument("--rows", default = 20, type = int, help = "Количество строчек на поле")
    parser.add_argument("--max_gens", type = int, help = "Максимальное количество поколений в игре")

    args = parser.parse_args()
    if args.max_gens:
        life = GameOfLife(size=(args.rows, args.cols), max_generations=args.max_gens)
    else:
        life = GameOfLife(size=(args.rows, args.cols))
    console=Console(life=life)
    console.run()
