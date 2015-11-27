# -*- coding: utf-8 -*-

from Tkinter import *
from ttk import Frame, Button

FONT = ('Lucida Console', '40')
FONT2 = ('Lucida Console', '24')
OPERATIONS = ('OR', 'AND', 'XOR', 'XAND')

LABELS = {'OR':'  A or B = ',
          'AND':' A and B = ',
          'XOR':' A xor B = ',
          'XAND': 'A xand B = '}

EXPRESSIONS = {'OR': lambda a,b: a | b,
               'AND': lambda a,b: a & b,
               'XOR': lambda a,b: a ^ b,
               'XAND': lambda a,b: 255 - (a ^ b)}


class BitWidget(Frame):
    """Класс для виджета из 1 бита."""

    def __init__(self, master, number, color='white', clicable=True,
                                                                 onChange=None):
        Frame.__init__(self, master, relief=GROOVE)
        self.label = Label(self, text='0', font=FONT, bg=color, fg='#555555')
        self.label.pack(ipadx=2, ipady=2, padx=1, pady=2)
        self.degree = number
        self.value = 0
        if clicable:
            self.label.bind('<Button-1>', self.click)
            self.label.bind('<Button-3>', self.click)
        self.parent = master
        self.onChange = onChange


    def click(self, event):
        """Изменить данные после клика мыши."""

        if self.value:
            self.value = 0
        else:
            self.value = 1
        self.label['text'] = str(self.value)
        self.parent.renew()
        if self.onChange:
            self.onChange()


    def set(self, value):
        """Установить значение бита принудительно."""

        self.value = value
        self.label['text'] = str(self.value)


class ByteWidget(Frame):
    """Класс для виджета из 8 битов."""

    def __init__(self, master, text=None, color='white', clicable=True,
                                                                 onChange=None):
        Frame.__init__(self, master, relief=GROOVE)
        self.value = 0
        if text:
            self.text = Label(self, text=text, font=FONT2)
            self.text .pack(side=LEFT, padx=2)
        self.bits = []
        for q in range(7, -1, -1):
            self.bits.append(BitWidget(self, number=q, color=color,
                                          onChange=onChange, clicable=clicable))
            self.bits[-1].pack(side=LEFT)
            if q == 4:
                Label(self, text='').pack(side=LEFT)
        Label(self, text=' = ', font=FONT2).pack(side=LEFT)
        self.dec = Label(self, text='0', font=FONT2, width=3, justify=LEFT,
                                                                       anchor=W)
        self.dec.pack(side=LEFT)


    def set(self, value):
        """Установить значение байта принудительно."""

        self.value = value
        sum = value
        self.dec['text'] = str(sum)
        for q in range(8):
            result = sum % 2
            sum /= 2
            self.bits[7-q].set(result)

    def renew(self):
        """Обновить значения после изменения битов."""

        sum = 0
        for q in self.bits:
            if q.value:
                sum += 2**q.degree
        self.value = sum
        self.dec['text'] = str(sum)


#-------------------------------

def calculate(event=None):
    """Подсчитать побитное выражение."""

    operation = bitFunctionList.selection_get()
    num = EXPRESSIONS[operation](first.value, second.value)
    third.set(num)


def reset():
    """Сбросить все значения байтов в ноль."""

    first.set(0)
    second.set(0)
    third.set(0)


def onChange(event):
    """Сменить операцию."""

    third.text['text'] = LABELS[bitFunctionList.selection_get()]
    calculate()

#----------------------------------- MAIN -------------------------------------%

root = Tk()
root.title(u'Побитовые операции: просто и наглядно')
root.resizable(width=False, height=False)

bitFunctionList = Listbox(root, height=4, width=4, font=FONT2,
                                      selectmode='single', activestyle='dotbox')
bitFunctionList.grid(column=1, row=1, rowspan=2, ipadx=5, ipady=2, padx=10,
                                                                        pady=10)
bitFunctionList.insert(END, *OPERATIONS)
bitFunctionList.bind('<ButtonRelease-1>', onChange)
bitFunctionList.selection_set(0)

first = ByteWidget(root, text='A = ', color='#ffffee', onChange=calculate)
first.grid(column=2, row=1, ipadx=2, ipady=2, padx=10, pady=10, sticky=E)
second = ByteWidget(root, text='B = ', color='#ffffee', onChange=calculate)
second.grid(column=2, row=2, ipadx=2, ipady=2, padx=10, pady=10, sticky=E)
third = ByteWidget(root, text='  A or B = ', color='#f5fff5', clicable=False)
third.grid(column=1, row=3, columnspan=2, sticky=E, ipadx=2, ipady=2, padx=10,
                                                                        pady=10)

Button(root, text=u'Сброс', command=reset).grid(column=2, row=4, ipadx=2,
                                            ipady=2, padx=10, pady=10, sticky=E)
root.mainloop()