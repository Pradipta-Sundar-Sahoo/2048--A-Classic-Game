import tkinter as tk
from tkinter import Frame, Label, CENTER

import Logics
import constants as c


class Game2048(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        self.grid()
        self.master.title('2048')
        self.master.bind("<Key>", self.key_down)
        self.commands = {
            c.KEY_UP: Logics.move_up,
            c.KEY_DOWN: Logics.move_down,
            c.KEY_LEFT: Logics.move_left,
            c.KEY_RIGHT: Logics.move_right
        }

        self.grid_cells = []
        self.init_grid()
        self.init_matrix()
        self.update_grid_cells()

        self.init_controls()

    def init_grid(self):
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME,
                           width=c.SIZE, height=c.SIZE)
        background.grid()

        for i in range(c.GRID_LEN):
            grid_row = []
            for j in range(c.GRID_LEN):
                cell = Frame(background, bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                             width=c.SIZE / c.GRID_LEN,
                             height=c.SIZE / c.GRID_LEN)
                cell.grid(row=i, column=j, padx=c.GRID_PADDING,
                          pady=c.GRID_PADDING)
                t = Label(master=cell, text="",
                          bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                          justify=CENTER, font=c.FONT, width=5, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def init_matrix(self):
        self.matrix = Logics.start_game()
        Logics.add_new_2(self.matrix)
        Logics.add_new_2(self.matrix)

    def update_grid_cells(self):
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(
                        text="", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(
                        text=str(new_number),
                        bg=c.BACKGROUND_COLOR_DICT[new_number],
                        fg=c.CELL_COLOR_DICT[new_number]
                    )
        self.update_idletasks()

    def key_down(self, event):
        key = repr(event.char)
        if key in self.commands:
            self.flicker_button(event.char)  # Add flicker effect
            self.matrix, changed = self.commands[key](self.matrix)
            if changed:
                Logics.add_new_2(self.matrix)
                self.update_grid_cells()
                if Logics.get_current_state(self.matrix) == 'WON':
                    self.grid_cells[1][1].configure(
                        text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(
                        text="Win!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                if Logics.get_current_state(self.matrix) == 'LOST':
                    self.grid_cells[1][1].configure(
                        text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(
                        text="Lose!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)

    def init_controls(self):
        control_frame = Frame(self)
        control_frame.grid(row=c.GRID_LEN, column=0, columnspan=c.GRID_LEN)

        button_size = 2
        button_font = ("Verdana", 20, "bold")
        button_color = c.BACKGROUND_COLOR_GAME
        flicker_color = "#FFA07A"  # Light orange color

        self.buttons = {
            'w': tk.Button(control_frame, text='W', width=button_size, height=button_size, font=button_font, bg=button_color, command=lambda: self.on_button_click('w')),
            'a': tk.Button(control_frame, text='A', width=button_size, height=button_size, font=button_font, bg=button_color, command=lambda: self.on_button_click('a')),
            's': tk.Button(control_frame, text='S', width=button_size, height=button_size, font=button_font, bg=button_color, command=lambda: self.on_button_click('s')),
            'd': tk.Button(control_frame, text='D', width=button_size, height=button_size, font=button_font, bg=button_color, command=lambda: self.on_button_click('d')),
        }

        for button in self.buttons.values():
            button.grid_propagate(False)  # Prevent resizing
            button.config(borderwidth=0, relief="solid", highlightthickness=0)
            button.bind("<Button-1>", self.on_button_click)
            button.config(highlightbackground=button_color)

        self.buttons['w'].grid(row=0, column=1, padx=5, pady=5)
        self.buttons['a'].grid(row=1, column=0, padx=5, pady=5)
        self.buttons['s'].grid(row=1, column=1, padx=5, pady=5)
        self.buttons['d'].grid(row=1, column=2, padx=5, pady=5)

    def on_button_click(self, event):
        key = event.widget.cget('text').lower()
        self.flicker_button(key)
        event = tk.Event()
        event.char = key
        self.key_down(event)

    def flicker_button(self, key):
        button = self.buttons[key]
        original_bg = button.cget('bg')
        flicker_color = "#FFA07A"  # Light orange color
        button.config(bg=flicker_color)
        self.after(100, lambda: button.config(bg=original_bg))


if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(master=root)
    game.mainloop()
