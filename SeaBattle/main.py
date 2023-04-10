import tkinter

import gui
import gamepole as 
import utils
from functools import partial


class SeaBattle:
    def __init__(self):
        self.gp1 = sb.GamePole(10)
        self.gp2 = sb.GamePole(10)
        self.gui_app = gui.MainWindow()

        # Properties
        self.gui_app.gamepolegui_player1.is_hidden = True

        # Buttons
        self.gui_app.start_button.bind('<Button-1>', self.start_game)
        self.gui_app.stop_game.bind('<Button-1>', self.stop_game)
        self.gui_app.random_button.configure(command=self.generate_and_draw_ships)

        # Cells
        self.configure_cells(self.gui_app.gamepolegui_player2)
        self.configure_cells(self.gui_app.gamepolegui_player1)

        # Status
        self.status_text = tkinter.StringVar()
        self.status_text.set("Welcome, comrade!")
        self.gui_app.status.configure(textvariable=self.status_text, background='#497e76')

    def configure_cells(self, gamepolegui: gui.GamePoleGui):
        for row_index in range(10):
            for column_index in range(10):
                gamepolegui.cells[row_index][column_index].configure(
                    command=partial(self.cell_pressed, utils.Point(column_index, row_index)),
                    state='disabled')

    def generate_and_draw_ships(self):
        # initializing (generating) game poles
        while True:
            try:
                self.gp1.init()
                self.gp2.init()
                break
            except ValueError:
                pass

        self.redraw_gamepole1()
        self.redraw_gamepole2()

        self.gui_app.start_button.configure(state='enabled')

    def redraw_gamepole1(self):
        self.gui_app.gamepolegui_player1.clear()
        for ship in self.gp1.get_ships():
            self.gui_app.gamepolegui_player1.draw_ship(ship)

    def redraw_gamepole2(self):
        self.gui_app.gamepolegui_player2.clear()
        for ship in self.gp2.get_ships():
            self.gui_app.gamepolegui_player2.draw_ship(ship)

    def cell_pressed(self,  point: utils.Point):
        self.hit(point)
        if not self.referee():
            self.move_and_redraw_ships()
            self.change_turn()

    def hit(self, point: utils.Point):
        if self.gui_app.gamepolegui_player1.is_enabled:
            self.gp1.hit(point)
        else:
            self.gp2.hit(point)

    def move_and_redraw_ships(self):
        if self.gui_app.gamepolegui_player1.is_enabled:
            self.gp1.move_ships()
            self.redraw_gamepole1()
        else:
            self.gp2.move_ships()
            self.redraw_gamepole2()

    def change_turn(self):
        if self.gui_app.gamepolegui_player1.is_enabled:
            self.gui_app.gamepolegui_player1.enabled(False)
            self.gui_app.gamepolegui_player2.enabled(True)
        else:
            self.gui_app.gamepolegui_player1.enabled(True)
            self.gui_app.gamepolegui_player2.enabled(False)

    def start_game(self, event):
        self.gui_app.gamepolegui_player1.enabled(True)
        self.status_start()
        self.gui_app.random_button.configure(state='disabled')

        print("Game started")

    def referee(self) -> bool:
        if all([ship.is_destroyed() for ship in self.gp1.get_ships()]):
            print("Player 2 win")
            self.stop_game()
            return True
        elif all([ship.is_destroyed() for ship in self.gp2.get_ships()]):
            print("Player 1 win")
            self.stop_game()
            return True
        return False

    def stop_game(self, event=None):
        self.gui_app.gamepolegui_player1.enabled(False)
        self.gui_app.gamepolegui_player2.enabled(False)
        self.status_stop()
        self.gui_app.random_button.configure(state='enabled')
        print("Game end")

    def status_start(self):
        self.status_text.set("STARTED")
        self.gui_app.status.configure(background='#009a63')

    def status_stop(self):
        self.status_text.set("STOPPED")
        self.gui_app.status.configure(background='#c94449')

    def run_app(self):
        self.gui_app.run()


if __name__ == "__main__":
    game = SeaBattle()
    game.run_app()
