# -*- coding: utf-8 -*-

from Tkinter import *

class Megabutton(Canvas):

    def __init__(self, parent, text='', command=None, top=2, depth=3, bound=10,
                font=('Verdana','14'), bg="#cccccc", shadow="#444444",
                act_bg="#e6e6e6", fg='black', active=True, press=None, **kargs):
        u"""Создает оригинальную кнопку. Параметры:
            text- строка текста, надпись на кнопке;
            command- функция. вызваемая при нажатии кнопки;
            depth - "глубина" кнопки;
            bound - внутренний отступ кнопки;
            font - шрифт текста;
            fg, bg, shadow, press, act_bg - цвета текста шрифта, фона, тени,
                нажатого фона и фона при наведении мыши соответственно;
            active - параметр, указывающий, будет ли кнопка менять цвет при
                наведении на нее мышью и/или нажатии."""

        temp = Canvas(parent)
        temp.create_text(0,0, text=text, font=font)
        box = temp.bbox(1)
        temp.destroy()

        width = box[2] - box[0] + bound * 2
        height = box[3] - box[1] + bound * 2
        if depth == None:
            depth = top + 1
        if depth < 0:
            depth = 4
        if top < 0:
            top = 3
        if press == None:
            press = act_bg

        Canvas.__init__(self, parent, height=height+top+1, width=width+top+1)

        (self.depth, self.top, self.bg, self.fg, self.shadow, self.act_bg,
        self.active, self.press) = (depth, top, bg, fg, shadow, act_bg, active,
        press)

        self.pressed = False

        self.create_rectangle(top+1, top+1, width+top+1, height+top+1, fill=shadow)
        self.create_rectangle(0, 0, width, height, fill=bg)
        self.create_text(width / 2, height / 2, text=text, font=font, fill=fg)

        self.bind('<Button-1>', self.onPress)
        self.bind('<ButtonRelease-1>', self.onRelease)
        if active:
            self.bind('<Enter>', self.onMouseOn)
            self.bind('<Leave>', self.onMouseOff)
        self.command = command


    def onMouseOn(self, event):
        if not self.pressed:
            self.itemconfig(2, fill=self.act_bg)


    def onMouseOff(self, event):
        if not self.pressed:
            self.itemconfig(2, fill=self.bg)


    def onPress(self, event):
        self.pressed = True
        self.move(3, self.depth, self.depth)
        self.move(2, self.depth, self.depth)
        if self.active:
            self.itemconfig(2, fill=self.press)


    def onRelease(self, event):
        self.pressed = False
        self.move(3, -self.depth, -self.depth)
        self.move(2, -self.depth, -self.depth)
        if (event.x > 0 and event.y > 0 and event.x <= self.winfo_width() and
                                            event.y <= self.winfo_height()):
            if self.active:
                self.itemconfig(2, fill=self.act_bg)
            else:
                self.itemconfig(2, fill=self.bg)
            if self.command:
                self.command()
        else:
            self.itemconfig(2, fill=self.bg)


if __name__ == '__main__':
    root = Tk()
    Megabutton(root, text='Hello world').grid(column=1, row=1)
    Megabutton(root, text=u'без подсветки', top=4, depth=3, bound=5, active=False).grid(column=1, row=2)
    Megabutton(root, text='Quit', top=10, depth=14, act_bg='yellow', command=root.destroy).grid(column=2, row=4)
    Megabutton(root, text='to Hell...', depth=13, press='#FF5533').grid(column=1, row=3)
    root.geometry('400x300+200+100')
    root.mainloop()