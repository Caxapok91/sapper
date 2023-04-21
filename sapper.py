from tkinter import *
import random
from tkinter.messagebox import showinfo, showerror
import time
import re


class Mybutton(Button):

    def __init__(self, master, x, y, number=0, *args, **kwargs):
        super(Mybutton, self).__init__(master, width=3, font='Calibri 15 bold', *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.count_bomb = 0
        self.is_open = False
        self.count_flag = 0
        self.time_start = 0
        self.is_flag = False


class Saper:
    window = Tk()
    window.title('Saper')
    ROW = 5
    COLUMNS = 5
    MINES = 5
    IS_GAMEROVER = False
    IS_FIRST_CLICK = True

    def __init__(self):
        self.buttons = []
        for i in range(self.ROW + 2):
            temp = []
            for j in range(self.COLUMNS + 2):
                btn = Mybutton(self.window, x=i, y=j)
                btn.config(command=lambda button=btn: self.click(button))
                btn.bind('<Button-3>', self.right_click)
                temp.append(btn)
            self.buttons.append(temp)

    def create_widgets(self):
        count = 1
        self.falg_position = []
        self.count_flag = self.MINES
        menubar = Menu(self.window)
        self.window.config(menu=menubar)
        settings_menu = Menu(menubar, tearoff=0)
        settings_menu.add_command(label='Start', command=self.reload)
        settings_menu.add_command(label='Settings', command=self.create_setting_win)
        settings_menu.add_command(label='Statistics', command=self.create_stat_win)
        settings_menu.add_command(label='Exit', command=self.window.destroy)
        menubar.add_cascade(label='Menu', menu=settings_menu)

        for i in range(1, self.ROW + 1):
            for j in range(1, self.COLUMNS + 1):
                btn = self.buttons[i][j]
                btn.number = count
                btn.grid(row=i, column=j, stick='NWES')
                count += 1
        for i in range(1, self.ROW + 1):
            Grid.rowconfigure(self.window, i, weight=1)
        for i in range(1, self.COLUMNS + 1):
            Grid.rowconfigure(self.window, i, weight=1)

        self.lbl_time = Label(text='click button')
        self.lbl_time.grid(row=0, column=1, columnspan=(self.COLUMNS // 2))
        self.lbl_mine = Label(text=f'Flags {self.count_flag}')
        self.lbl_mine.grid(row=0, column=(self.COLUMNS // 2) + 1, columnspan=(self.COLUMNS // 2))

    def create_setting_win(self):
        def change_lvl(mines, row, col):
            row_entry.delete(0, END)
            row_entry.insert(0, row)
            column_entry.delete(0, END)
            column_entry.insert(0, col)
            mines_entry.delete(0, END)
            mines_entry.insert(0, mines)

        win_settings = Toplevel(self.window)
        win_settings.title('Settings')
        Label(win_settings, text='Count row').grid(row=0, column=0)
        Label(win_settings, text='Count column').grid(row=1, column=0)
        Label(win_settings, text='Count mines').grid(row=2, column=0)

        row_entry = Entry(win_settings)
        row_entry.insert(0, self.ROW)
        row_entry.grid(row=0, columnspan=3, column=1, padx=20, pady=20)
        column_entry = Entry(win_settings)
        column_entry.insert(0, self.COLUMNS)
        column_entry.grid(row=1, columnspan=3, column=1, padx=20, pady=20)
        mines_entry = Entry(win_settings)
        mines_entry.insert(0, self.COLUMNS)
        mines_entry.grid(row=2, columnspan=3, column=1, padx=20, pady=20)

        save_btn = Button(win_settings, text='Apply',
                          command=lambda: self.change_settings(row_entry, column_entry, mines_entry))
        save_btn.grid(row=4, column=1, padx=20, pady=20)

        easy_btn = Button(win_settings, text='Easy', command=lambda: change_lvl(5, 6, 6))
        easy_btn.grid(row=3, column=0)

        normal_btn = Button(win_settings, text='Normal', command=lambda: change_lvl(10, 10, 10))
        normal_btn.grid(row=3, column=1)

        hard_btn = Button(win_settings, text='Hard', command=lambda: change_lvl(35, 10, 25))
        hard_btn.grid(row=3, column=2)

    def reload(self):
        [child.destroy() for child in self.window.winfo_children()]
        self.__init__()
        self.create_widgets()
        self.IS_GAMEROVER = False
        self.IS_FIRST_CLICK = True

    def change_settings(self, row: Entry, column: Entry, mines: Entry):
        try:
            int(row.get()), int(column.get()), int(column.get())
        except ValueError:
            showerror('Error', 'Incorrect values')
            return
        self.ROW = int(row.get())
        self.COLUMNS = int(column.get())
        self.MINES = int(mines.get())
        self.reload()

    def create_stat_win(self):
        with open('logs.txt', 'r') as logs:
            text = logs.read()
            list_game_time = re.findall(r':(\w+)', text)
            list_game_result = re.findall(r'-(\w+)', text)
        time = 0
        for i in list_game_time:
            time += int(i)
        time_avg = time / len(list_game_time)
        win_avg = list_game_result.count('win') / len(list_game_result)
        showinfo('Statistics', f'You plaed {len(list_game_result)}\n'
                               f'You win rating {win_avg * 100}%\n'
                               f'Average game time {time_avg:.2f} sec')

    def right_click(self):
        pass

    def click(self, clicked_button: Mybutton):
        print(clicked_button.number)

        with open('logs.txt', 'a') as logs:
            logs.write(f'result-win time:{random.randrange(20)}\n')
        if self.IS_GAMEROVER:
            return
        if self.IS_FIRST_CLICK:
            self.time_start = time.time()
            self.insert_mines(clicked_button.number)
            self.print_mines()
            self.tick()
            self.IS_FIRST_CLICK = False
        if not clicked_button.is_mine:
            clicked_button.config(text = 0,disabledforeground='black')
            clicked_button.is_open = True
        else:
            clicked_button.config(text="*",disabledforeground='black')
            clicked_button.is_open = True
        clicked_button.config(foreground='black',relief = SUNKEN)
    def get_mine_places(self, exlude_number: int):
        indexes = list(range(1, self.COLUMNS * self.ROW + 1))
        indexes.remove(exlude_number)
        random.shuffle(indexes)
        return indexes[:self.MINES]

    def insert_mines(self, number: int):
        self.index_mines = self.get_mine_places(number)
        print(f'mines in {self.index_mines}')
        for i in range(1, self.ROW + 1):
            for j in range(1, self.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.number in self.index_mines:
                    btn.is_mine = True

    def print_mines(self):
        for i in range(1, self.ROW + 1):
            for j in range(1, self.COLUMNS):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    print("b", end='')
                else:
                    print(btn.count_bomb, end='')
            print()

    def tick(self):
        if self.IS_GAMEROVER:
            return
        timer = time.time() - self.time_start
        self.lbl_time.config(text=f'Time:{timer:.0f}')
        self.lbl_time.after(500, self.tick)

    def start(self):
        self.create_widgets()
        self.window.mainloop()


game = Saper()
game.start()
