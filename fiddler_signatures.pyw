
import hashlib
from Tkinter import *
from ttk import Button, Style
from tkMessageBox import showinfo


class Settings(object):
    """Mixin class with settings of application.
    """
    _FONT = ('Verdana', '12')
    _ENTRY_WIDTH = 50
    _PAD_X = 5
    _PAD_Y = 5
    _KEY_OF_SIGNATURE_PARAMS = 'mysigparams'
    _KEY_OF_SIGNATURE = 'mysig'
    _KEY_OF_SESSION_ID = 'sessionid'
    _NETWORK = 'odnoklassniki'


# --------------------- PRESENTER ------------------------- #


class Main(Settings):
    """Presenter: middleware between view and model.
    """
    def __init__(self):
        """Create instances of Model and View. Start GUI mainloop.
        """
        self.gui = View(callback=self.handle_signature_params_entering)
        self.model = Model()
        self.gui.start()


    def handle_signature_params_entering(self, tkinter_event):
        """[Handler] of case when signature params is entered.
        """
        request_params = self._get_signature_params()
        if request_params:
            self.gui.create_params_entries(request_params)
            self.gui.disable_param_entry(self._KEY_OF_SIGNATURE_PARAMS)
            self.gui.create_run_button(
                   text='Verify', callback=self.handle_verify_button_pressing)


    def handle_verify_button_pressing(self):
        """[Handler] of "Verify" button.
        """
        if self.model.verify_signature(self.gui.get_all_params_values()):
            self.gui.change_param_entry_bg(param_name='mysig', color='yellow')
            self.gui.modify_run_button(text='Calculate',
                               callback=self.handle_calculate_button_pressing)
        else:
            showinfo(title='Error', message='Something goes wrong!')


    def handle_calculate_button_pressing(self):
        """[Handler] of "Calculate" button.
        """
        params_dict = self.gui.get_all_params_values()
        signature = self.model.calculate_signature(params_dict)
        self.gui.set_param_value(self._KEY_OF_SIGNATURE, signature)


    def _get_signature_params(self):
        """Form list of signature params from according entry.
        """
        sig_params_string = self.gui.get_param_value(
                                                 self._KEY_OF_SIGNATURE_PARAMS)
        if not sig_params_string:
            return []
        else:
            return sig_params_string.strip().split('|')


# --------------------- MODEL ------------------------- #


class Model(Settings):
    """Application logic.
    """
    def calculate_signature(self, raw_params):
        """Calculate a signature for Pirate Treasures.
        """
        params = self._get_filtered_params(raw_params)
        if (not all(params)) or (not params[self._KEY_OF_SESSION_ID].isdigit()):
            return None
        key_list = sorted(params.keys())
        value_list = [params[key].strip() for key in key_list]
        postfix = str((int(params[self._KEY_OF_SESSION_ID]) + 1) << 5)
        string = self._NETWORK + ''.join(value_list) + postfix
        _hash = hashlib.md5(string)
        return _hash.hexdigest()


    def verify_signature(self, raw_params):
        """Check, if signature is calculated according to implemented
        logic.
        """
        signature = raw_params[self._KEY_OF_SIGNATURE]
        return signature == self.calculate_signature(raw_params)


    def _get_filtered_params(self, raw_params):
        """Filter request params to reach the list of them, have to
        be used in signature calculation.
        """
        return {key:raw_params[key] for key in raw_params
                if not(key == self._KEY_OF_SIGNATURE_PARAMS or
                       key == self._KEY_OF_SIGNATURE)}

# --------------------- VIEW ------------------------- #

class View(Settings):
    """GUI class.
    """
    # GUI constraints
    _FIRST_COLUMN = 0
    _SECOND_COLUMN = 1

    def __init__(self, callback):
        """Creates first (short) variant of GUI.
        Only one entry for "mysigparams" string.
        Bind 'callback' to be called afer string will be entered.
        """
        # ~ attributes ~
        self._params_entries = {}
        self._rows_count = 0

        # ~ main window section ~
        self._root = Tk()
        self._root.title('Signature generator')
        self._root.resizable(False, False)

        # ~ "mysigparams" section
        self._create_param_line(param_name=self._KEY_OF_SIGNATURE_PARAMS)
        self._params_entries[self._KEY_OF_SIGNATURE_PARAMS].bind(
                                                          "<Return>", callback)

    def start(self):
        """Start GUI mainloop.
        """
        self._root.mainloop()


    def create_params_entries(self, request_params_list):
        """Make full list of params entries in form.
        """
        for param_name in request_params_list:
            self._create_param_line(param_name)
        self._create_param_line(self._KEY_OF_SIGNATURE)
        self._create_param_line(self._KEY_OF_SESSION_ID)


    def disable_param_entry(self, param_name):
        """Make some param entry "gray" and unaccessible.
        """
        self._params_entries[param_name].configure(state='disabled')


    def change_param_entry_bg(self, param_name, color):
        """Change background color of some param entry.
        """
        self._params_entries[param_name].configure(background=color)


    def get_param_value(self, param_name):
        """Get single param value by it's name
        """
        return self._params_entries[param_name].get()


    def set_param_value(self, param_name, value):
        """Set param value in according entry.
        """
        self._params_entries[param_name].delete(0, END)
        self._params_entries[param_name].insert(0, value)


    def get_all_params_values(self):
        """Get dict of params values in format:
            {<param name> : <param value>}
        """
        return {entry_name: self._params_entries[entry_name].get()
                                        for entry_name in self._params_entries}


    def create_run_button(self, text, callback):
        """Create "magic button" to confirm operations.
        """
        # ~ style ~
        style = Style()
        style.configure('Run.TButton', font='verdana 12')

        # ~ button ~
        self.run_button = Button(text=text, command=callback,
                                                           style='Run.TButton')
        self.run_button.grid(column=self._SECOND_COLUMN, row=self._rows_count,
                             padx=self._PAD_X, pady=self._PAD_Y)


    def modify_run_button(self, text, callback):
        """Change "magic button" text and callback.
        """
        self.run_button.configure(text=text, command=callback)


    def _create_param_line(self, param_name):
        """Create line of label with param name and param entry.
        Register param in whole params list.
        """
        new_entry = Entry(self._root, width=self._ENTRY_WIDTH, font=self._FONT)
        new_entry.grid(column=self._SECOND_COLUMN, row=self._rows_count,
                       padx=self._PAD_X, pady=self._PAD_Y)
        mysigparams_label = Label(self._root, text=param_name, font=self._FONT)
        mysigparams_label.grid(column=self._FIRST_COLUMN, row=self._rows_count,
                               padx=self._PAD_X, pady=self._PAD_Y)
        self._params_entries[param_name] = new_entry
        self._rows_count += 1


# -------------------------------

z = Main()