import curses

from life import GameOfLife
from ui import UI
import time

class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        curses.resize_term(self.life.rows + 2, self.life.cols + 2)
        screen.border('|', '|', '-', '-', '+', '+', '+', '+')

    def draw_grid(self, screen) -> None:
        for y,line in enumerate(self.life.curr_generation):
            newline = ""
            for c in line:
                if c:
                    newline += "*"
                else:
                    newline += " "
            screen.addstr(y+1, 1, newline)

    def run(self) -> None:
        while self.life.is_changing and not self.life.is_max_generations_exceeded:
            screen = curses.initscr()
            screen.clear()
            self.draw_borders(screen)
            self.draw_grid(screen)
            self.life.step()
            screen.refresh()
            time.sleep(0.5)
        curses.endwin()
if __name__ == "__main__":
    cols=int(input('cols\n'))
    rows=int(input('rows\n'))
    max_gens=int(input('maximum generations or \'0\' for infinity\n'))
    if max_gens == 0:
        life=GameOfLife(size=(rows,cols))
    else:
        life=GameOfLife(size=(rows,cols), max_generations=max_gens)
    console=Console(life=life)
    console.run()
