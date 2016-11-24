

import hashlib
from Tkinter import *
from tkMessageBox import showinfo


def make_signature(params, session_id):
    """Calc a signature for Pirate Treasures
    """
    network = 'odnoklassniki';
    key_list = params.keys()
    key_list.sort()
    value_list = [params[key].strip() for key in key_list]
    postfix =  str((int(session_id) + 1) << 5)
    string = network + ''.join(value_list) + postfix
    _hash = hashlib.md5(string)
    return _hash.hexdigest()


def split(event):
    """
    """
    string = entry_mysigparams.get()
    params = string.strip().split('|')
    entry_mysigparams.configure(state='disabled')
    global params_dict
    params_dict = {}
    row = 1
    if params <> ['']:
        for param in params:
            params_dict[param] = Entry(root, width=50, font=FONT)
            Label(root, text=param, font=FONT).grid(column=0,
                                                        row=row, padx=5, pady=5)
            params_dict[param].grid(column=1, row=row, padx=5, pady=5)
            row += 1

    params_dict['mysig'] = Entry(root, width=50, font=FONT)
    Label(root, text='mysig', font=FONT).grid(column=0, row=row, padx=5, pady=5)
    params_dict['mysig'].grid(column=1, row=row, padx=5, pady=5)

    row += 1

    params_dict['sessionid'] = Entry(root, width=50, font=FONT)
    Label(root, text='sessionid', font=FONT).grid(column=0,
                                                        row=row, padx=5, pady=5)
    params_dict['sessionid'].grid(column=1, row=row, padx=5, pady=5)

    global button_verify
    button_verify = Button(text='Verify', command=verify, font=FONT)
    button_verify.grid(column=1, row=20, padx=5, pady=5)


def verify():
    """
    """
    params = {}
    for key, entry in params_dict.items():
        if key == 'mysig':
            mysig = entry.get()
        elif key == 'sessionid':
            sessionid = entry.get()
        else:
            params[key] = entry.get()
    if mysig == make_signature(params, sessionid):
        params_dict['mysig'].configure(background='yellow')
        button_verify.configure(text='Calculate', command=calculate)
    else:
        showinfo(title='Error', message='Something goes wrong!')


def calculate():
    """
    """
    params = {}
    for key, entry in params_dict.items():
        if key == 'mysig':
            mysig = entry.get()
        elif key == 'sessionid':
            sessionid = entry.get()
        else:
            params[key] = entry.get()

    params_dict['mysig'].delete(0,END)
    params_dict['mysig'].insert(0, make_signature(params, sessionid))


#------------------------------------ main ----------------------------------- #

root = Tk()
root.title('Signature generator')
root.resizable(False, False)

FONT = ('Verdana', '14')

Label(root, text='mysigparams', font=FONT).grid(column=0, row=0, padx=5, pady=5)
entry_mysigparams = Entry(root, width=50, font=FONT)
entry_mysigparams.grid(column=1, row=0, padx=5, pady=5)
entry_mysigparams.bind("<Return>", split)


root.mainloop()