# -*- coding: utf-8 -*-

from Tkinter import *
from ttk import Frame, Button


FONT = ('Lucida Console', '40')
FONT2 = ('Courier', '40', 'bold')

HEX = ('0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F')
COLORS = ('#fff5f5', '#f5fff5', '#f5f5ff', '#ffffee')


class BitWidget(Frame):

    def __init__(self, master, number, color='white'):
        Frame.__init__(self, master, relief=GROOVE)
        self.label = Label(self, text='0', font=FONT, bg=color, fg='#555555')
        self.label.pack(ipadx=2, ipady=2, padx=1, pady=2)
        self.degree = number
        self.value = 0
        self.label.bind('<Button-1>', self.click)
        self.label.bind('<Button-3>', self.click)
        self.info = Label(self, text=str(2**number), font=('Arial Narrow', '12'))
        self.info.pack(pady=2)

    def click(self, event):
        if self.value:
            self.value = 0
        else:
            self.value = 1
        self.label['text'] = str(self.value)
        change_str()
        change_hex()


    def set(self, value):
        self.value = value
        self.label['text'] = str(self.value)


class HexWidget(Frame):

    def __init__(self, master, number, color='white'):
        Frame.__init__(self, master, relief=GROOVE)
        self.label = Label(self, text='0', font=FONT2, bg=color, fg='#555555')
        self.label.pack(ipadx=2, ipady=2, padx=1, pady=2)
        self.degree = number
        self.value = 0
        self.label.bind('<Button-1>', self.click)
        self.label.bind('<Button-3>', self.click2)


    def click(self, event):
        self.value += 1
        if self.value > 15:
            self.value = 0
        self.label['text'] = HEX[self.value]
        change_bit()
        change_str()


    def click2(self, event):
        self.value -= 1
        if self.value < 0:
            self.value = 15
        self.label['text'] = HEX[self.value]
        change_bit()
        change_str()


    def set(self, value):
        self.value = value
        self.label['text'] = HEX[self.value]


class DecWidget(Frame):

    def __init__(self, master):
        Frame.__init__(self, master, relief=GROOVE)
        self.label = Label(self, text='0', width=5, font=FONT, anchor=E,
                                                       bg='white', fg='#555555')
        self.label.pack(ipadx=2, ipady=2, padx=1, pady=2)
        self.info = Label(self, text='', font=('Arial Narrow', '12'))
        self.info.pack(pady=2)
        self.value = 0

    def change(self, value, string):
        self.label['text'] = str(value)
        self.info['text'] = string
        self.value = value


#-------------------------------

def change_str():
    string = ''
    sum = 0
    for q in bytes_:
        if q.value:
            sum += 2**q.degree
            if not string:
                string += str(2**q.degree)
            else:
                string += ' + ' + str(2**q.degree)
    dec.change(sum, string)


def change_bit():
    sum = 0
    for q in hexes:
        sum += q.value * 16**q.degree
    for q in range(16):
        result = sum % 2
        sum /= 2
        bytes_[15-q].set(result)


def change_hex():
    hex_ = [0, 0, 0, 0]
    for q in bytes_:
        if q.value:
            hex_[q.degree // 4] += 2**(q.degree % 4)
    hex_.reverse()
    for item, value in zip(hexes, hex_):
        item.set(value)


def reset():
    for q in bytes_:
        q.set(0)
    change_hex()
    change_str()

#---------------------------------------------------------------------

root = Tk()
root.title(u'hex/dec/bin: просто и наглядно')
root.resizable(width=False, height=False)

byteFrame = Frame(root)
byteFrame.pack(padx=10, pady=5)

bytes_ = []
for q in range(15, -1, -1):
    bytes_.append(BitWidget(byteFrame, number=q, color=COLORS[q//4]))
    bytes_[-1].pack(side=LEFT)
    if q == 8:
        Label(byteFrame, text='   ').pack(side=LEFT)
    if q == 12 or q == 4:
        Label(byteFrame, text='').pack(side=LEFT)

hexFrame = Frame(root)
hexFrame.pack(pady=5)

hexes = []
for q in range(3, -1, -1):
    hexes.append(HexWidget(hexFrame, number=q, color=COLORS[q]))
    hexes[-1].pack(side=LEFT)
    if q == 2:
        Label(hexFrame, text='   ').pack(side=LEFT)

dec = DecWidget(root)
dec.pack(pady=5, expand=YES, fill=X)

Label(root, text=u'  Кликаем левой(правой) кнопкой мыши на значениях hex/bin'
                                    ).pack(side=LEFT)
Button(root, text=u'Сброс', command=reset).pack(side=RIGHT, padx=10, pady=10)

root.mainloop()