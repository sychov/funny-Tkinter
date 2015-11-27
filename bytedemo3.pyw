# -*- coding: utf-8 -*-

from Tkinter import *
from ttk import Frame, Button


FONT = ('Lucida Console', '40')
COLORS = ('#fff5f5', '#f5fff5', '#f5f5ff', '#ffffee')


class BitWidget(Frame):
    """Класс для виджета из 1 бита."""

    def __init__(self, master, number, color='white', onChange=None):
        Frame.__init__(self, master, relief=GROOVE)
        self.label = Label(self, text='0', font=FONT, bg=color, fg='#555555')
        self.label.pack(ipadx=2, ipady=2, padx=1, pady=2)
        self.degree = number
        self.value = 0
        self.label.bind('<Button-1>', self.click)
        self.label.bind('<Button-3>', self.click)
        self.info = Label(self, text=str(2**number), font=('Arial Narrow', '12'))
        self.info.pack(pady=2)
        self.onChange = onChange


    def click(self, event):
        """Изменить данные после клика мыши."""
        if self.value:
            self.value = 0
        else:
            self.value = 1
        self.label['text'] = str(self.value)
        if self.onChange:
            self.onChange()


    def set(self, value):
        """Установить значение бита принудительно."""
        self.value = value
        self.label['text'] = str(self.value)



class DecWidget(Frame):
    """Класс для десятичного представления значения."""

    def __init__(self, master):
        Frame.__init__(self, master, relief=GROOVE)
        self.label = Label(self, text='0', width=5, font=FONT, anchor=E,
                                                       bg='white', fg='#555555')
        self.label.pack(ipadx=2, ipady=2, padx=1, pady=2)
        self.value = 0


    def set(self, value):
        self.label['text'] = str(value)
        self.value = value


#-------------------------------

def reset():
    """Устанавливаем значение в 0."""
    for q in bytes_:
        q.set(0)
    dec.set(0)


def renew():
    """Обновляем десятичное значение."""
    sum = 0
    for q in bytes_:
        if q.value:
            sum += 2**q.degree
    dec.set(sum)


def shift_left():
    """Сдвигаем биты влево."""
    for q in range(15):
        bytes_[q].set(bytes_[q+1].value)
    bytes_[15].set(0)
    renew()


def shift_right():
    """Сдвигаем биты вправо."""
    for q in range(15, 0, -1):
        bytes_[q].set(bytes_[q-1].value)
    bytes_[0].set(0)
    renew()


def applyNot():
    """Инвертируем биты."""
    for q in range(15, -1, -1):
        if bytes_[q].value:
            bytes_[q].set(0)
        else:
            bytes_[q].set(1)
    renew()


#--------------------------------- MAIN ----------------------------------------


root = Tk()
root.title(u'<< not >>: просто и наглядно')
root.resizable(width=False, height=False)

byteFrame = Frame(root)
byteFrame.pack(padx=10, pady=5)

bytes_ = []
for q in range(15, -1, -1):
    bytes_.append(BitWidget(byteFrame, number=q, color=COLORS[q//4],
                                                              onChange = renew))
    bytes_[-1].pack(side=LEFT)
    if q == 8:
        Label(byteFrame, text='   ').pack(side=LEFT)
    if q == 12 or q == 4:
        Label(byteFrame, text='').pack(side=LEFT)

controlFrame = Frame(root)
controlFrame.pack(padx=10, pady=5, expand=YES, fill=X)

dec = DecWidget(controlFrame)
dec.pack(pady=5, padx=10, side=RIGHT)

Button(controlFrame, text='<<', command=shift_left).pack(padx=10, side=LEFT)
Button(controlFrame, text='NOT', command=applyNot).pack(padx=10, side=LEFT)
Button(controlFrame, text='>>', command=shift_right).pack(padx=10, side=LEFT)

Label(root, text=u'').pack(side=LEFT)
Button(root, text=u'Сброс', command=reset).pack(side=RIGHT, padx=10, pady=10)

root.mainloop()