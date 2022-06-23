import tkinter
from tkinter import messagebox
from PIL import ImageTk
import mysql.connector
import hashlib


"""qwerty = 12345
doctor = hi
ice = eye
root = root123
"""

"""  "; /*  """
"""*/ UPDATE logins SET password = "1" WHERE login = "qwerty"; -- """


class HomeScreen:
    """Create a home screen with a database connection"""

    def __init__(self, first, mydb=None):
        self.__mydb = mydb
        self.__root = tkinter.Tk()
        self.__first = first
        self.__dict = {}
        self.create()

    def create(self):
        self.__root.title('Авторизация')
        self.__root.resizable(False, False)
        if not self.__first:
            self.__root.geometry('560x330+450+150')
            a = ("USER", "HOST", "PASSWORD", "DATABASE")
            for i in a:
                k = a.index(i)
                tkinter.Label(self.__root, text=i + ":", font=("Arial", 14), fg="red").place(x=40, y=k*70+30)
                u = tkinter.Entry(self.__root, bg='white', font=('Arial', 14), width=35, relief=tkinter.GROOVE, show="*" if i == "PASSWORD" else "",
                                  fg='black', justify=tkinter.CENTER)
                u.place(x=180, y=70*k+30)
                self.__dict[i] = u
            tkinter.Button(self.__root, text="CONNECT", bg="yellow", width=10, font=("Arial", 14), command=self.bd_connect,
                           relief=tkinter.GROOVE).place(x=40, y=280)
            self.__root.mainloop()
        else:
            self.__root.geometry('700x530+450+150')
            color = '#212121'
            canvas = tkinter.Canvas(self.__root, width=700, height=530)
            canvas.pack()
            photo = ImageTk.PhotoImage(file='picture.jpg')
            canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)
            frame = tkinter.Frame(canvas, bg=color, width=600, height=440)
            canvas.create_window((350, 265), window=frame)
            Aplication(frame, self.__mydb, color)
            self.__root.mainloop()

    def bd_connect(self):
        try:
            self.__mydb = mysql.connector.connect(
                user=self.__dict["USER"].get(),
                host=self.__dict["HOST"].get(),
                password=self.__dict["PASSWORD"].get(),
                database=self.__dict["DATABASE"].get())
        except Exception as e:
            messagebox.showerror(title="Attention!!! Failed to connect to database", message=e)
            return None
        choice = messagebox.askyesno(title="Successful connection", message="Do you want to continue?")
        if choice:
            self.__root.destroy()
            HomeScreen(True, self.__mydb)

class Aplication:
    """Create an application"""
    def __init__(self, master, mydb, color):
        self.__frame = master
        self.__cur = mydb.cursor()
        self.__color = color
        self.__widget = {}
        self.__counter = 0
        self.__lst = []
        self.__update = True
        self.create()

    def create(self):
        tkinter.Label(self.__frame, text='Введите логин', fg='white', font=('Arial', 12), bg=self.__color).grid(column=0,
                                                                                                             row=0,
                                                                                                             sticky='NW')
        tkinter.Label(self.__frame, text='Введите пароль', fg='white', font=('Arial', 12), bg=self.__color).grid(column=0,
                                                                                                              row=1,
                                                                                                              sticky='NW',
                                                                                                              pady=10)
        self.__widget["label"] = tkinter.Label(self.__frame, text='', anchor='nw', fg='black', bg='white', font=('Arial', 10),
                                         width=80, height=17, relief=tkinter.GROOVE, borderwidth=3)
        self.__widget["label"].grid(row=5, column=0, sticky='NW', padx=15, columnspan=6, pady=10)
        self.create_main_bttn()

    def create_main_bttn(self):
        self.__widget["bttn_come"] = tkinter.Button(self.__frame, text='Войти', width=9, height=1,
                       bg='#82898f', fg='yellow', relief=tkinter.RAISED, font=('Arial', 11), command=self.enterance)
        self.__widget["bttn_brute"] = tkinter.Button(self.__frame, text='brute force', width=9, height=1,
                       bg='#82898f', fg='red', relief=tkinter.RAISED, font=('Arial', 11), command=self.brute)
        self.__widget["bttn_sql"] = tkinter.Button(self.__frame, text="SQL-injection", width=9, height=1,
                       bg="#82898f", fg="red", relief=tkinter.RAISED, font=('Arial', 11), command=self.injection)
        self.__widget["bttn_come"].grid(row=4, column=0, pady=10, sticky='NW')
        self.__widget["bttn_brute"].grid(row=4, column= 1, pady=10, sticky="NW")
        self.__widget["bttn_sql"].grid(row=4, column=1, padx = 108)
        if "login" not in self.__widget or not self.__widget["login"]:
            self.__widget["login"] = tkinter.Entry(self.__frame, bg='white', font=('Arial', 12), width=50,
                                                   relief=tkinter.GROOVE,
                                                   fg='black', justify=tkinter.CENTER)
            self.__widget["password"] = tkinter.Entry(self.__frame, bg='white', font=('Arial', 12), width=50,
                                                      relief=tkinter.GROOVE,
                                                      fg='black', justify=tkinter.CENTER)
            self.__widget["login"].grid(column=1, row=0, padx=10, columnspan=6)
            self.__widget["password"].grid(column=1, row=1, padx=10, columnspan=6)

    def enterance(self, exist = True):
        """button"""
        if exist:
            self.__cur.execute(
                f'SELECT * FROM logins WHERE login = "{self.__widget["login"].get()}" AND password = "{hashlib.md5(self.__widget["password"].get().encode()).hexdigest()}"')
        else:
            self.__cur.execute(
                f'SELECT * FROM logins WHERE login = "{self.__widget["login"]["text"]}" AND password = "{hashlib.md5(self.__widget["password"]["text"].encode()).hexdigest()}"')
        res = self.__cur.fetchall()
        if not res:
            if len(self.__widget["label"]['text'].split('\n')) > 17:
                self.__widget["label"]['text'] = ''
            self.__widget["label"]['text'] += 'ACCESS DENIED\n'
        else:
            if res[0][0] == 4:
                self.__cur.execute("SELECT * FROM logins ")
                result = self.__cur.fetchall()
                for a in result:
                    self.__widget["label"]['text'] += f'{a}' + '\n'
            if len(self.__widget["label"]['text'].split('\n')) > 17:
                self.__widget["label"]['text'] = 'ACCESS ALLOWED\n'
            else:
                self.__widget["label"]['text'] += 'ACCESS ALLOWED\n'
                if not exist:
                    self.__widget["label"]['text'] += self.__widget["login"]["text"] + " " + self.__widget["password"]["text"] + "\n"

    def brute(self):
        with open("brute.txt", "r") as file:
            a = file.read()
            a = a.split('\n')
            a.pop(-1)
        self.__widget["bttn_come"].destroy()
        self.__widget["bttn_brute"].destroy()
        self.__widget["bttn_sql"].destroy()
        self.__widget["login"].destroy()
        self.__widget["password"].destroy()
        self.__lst = [tkinter.Button(self.__frame, text="-->", width=9, height=1,
                    fg='red', relief=tkinter.RAISED, command=lambda a = a: self.next(a), font=('Arial', 11)),
               tkinter.Button(self.__frame, text="<--", width=9, height=1,
                    fg='red', relief=tkinter.RAISED, command=lambda a = a: self.back(a), font=('Arial', 11)),
               tkinter.Button(self.__frame, text="finish", width=9, height=1,
                    fg='red', relief=tkinter.RAISED, command=lambda a = a: self.finish(a), font=('Arial', 11))]
        self.__widget["login"] = tkinter.Label(self.__frame, width=50, bg='white', font=('Arial', 12), fg='black', justify=tkinter.CENTER)
        self.__widget["password"] = tkinter.Label(self.__frame, width=50, bg='white', font=('Arial', 12), fg='black', justify=tkinter.CENTER)
        self.__lst[0].grid(row=4, column=0, pady=10, sticky='NW')
        self.__lst[1].grid(row=4, column=1, pady=10, sticky='NW')
        self.__lst[2].grid(row=4, column=2, pady=10, sticky='NW')
        self.__widget["login"].grid(column=1, row=0, padx=10, columnspan=6)
        self.__widget["password"].grid(column=1, row=1, padx=10, columnspan=6)

    def next(self, a):
        if self.__counter >= 44:
            self.__counter = 0
        a = a[self.__counter].split()
        self.__widget["login"]["text"] = a[0]
        self.__widget["password"]["text"] = a[1]
        self.__counter += 1
        self.enterance(False)

    def back(self, a):
        if self.__counter <= 0:
            self.__counter = 43
        if self.__counter >= 44:
            self.__counter = 0
        a = a[self.__counter].split()
        self.__widget["login"]["text"] = a[0]
        self.__widget["password"]["text"] = a[1]
        self.__counter -= 1
        self.enterance(False)

    def finish(self, a):
        for i in a:
            i = i.split()
            self.__cur.execute(f'SELECT * FROM logins WHERE login = "{i[0]}" AND password = "{hashlib.md5(i[1].encode()).hexdigest()}"')
            res = self.__cur.fetchall()
            if res:
                self.__widget["label"]['text'] += 'ACCESS ALLOWED\n' + i[0] + " " + i[1] + '\n'
                break
        for i in self.__lst:
            i.destroy()
        self.__widget["login"].destroy()
        self.__widget["password"].destroy()
        self.__widget["login"] = False
        self.create_main_bttn()

    def injection(self):
        self.__update = True
        self.__widget["bttn_come"].destroy()
        self.__widget["bttn_brute"].destroy()
        self.__widget["bttn_sql"].destroy()
        self.__widget["bttn_sql"] = tkinter.Button(self.__frame, text='finish', width=9, height=1,
                       fg='red', relief=tkinter.RAISED, font=('Arial', 11), command=self.query)
        self.__widget["bttn_sql"].grid(row=4, column=0, pady=10, sticky='NW')
        while self.__update:
            self.__widget["label"]["text"] = f'SELECT * FROM logins WHERE\n login = "{self.__widget["login"].get()}" \nAND password = "' \
                                             f'{self.__widget["password"].get()}"'
            self.__frame.update()

    def query(self):
        self.__update = False
        self.__widget["label"]["text"] = self.__widget["label"]["text"].replace('\n', '')
        self.__cur.execute(self.__widget["label"]["text"])
        self.__widget["label"]["text"] = ''
        for i in self.__cur.fetchall():
            self.__widget["label"]["text"] += str(i) + '\n'
        self.__widget["bttn_sql"].destroy()
        self.create_main_bttn()


if __name__ == '__main__':
    HomeScreen(False)