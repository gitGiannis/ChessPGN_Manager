# -------------------------------------------------------------------------------------------------------------------- #
# _debugger.py: περιέχει την κλάση MyTest για τεστάρισμα αρχείων pgn                                                   #
# -------------------------------------------------------------------------------------------------------------------- #
from tkinter import Tk, Text
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Progressbar, Button, Frame, Label
from pgn import FilePGN
from game_loader import GameLoader


class MyTest(Tk):
    """
    Κλάση για τεστάρισμα αρχείων pgn (δε χρησιμοποιείται από το κυρίως πρόγραμμα)
    Τρέχει όλα τα παιχνίδια του αρχείου και κρατάει σε λίστα όσα από αυτά είχαν σφάλμα ή δεν έτρεξαν
    >> python -m PyInstaller --name="debugger" --icon=icons/debug.ico --noconsole --add-data="icons/debug.ico;icons"
    _debugger.py
    """
    def __init__(self):
        super().__init__()
        self.title("debugger")
        self.iconbitmap("icons\\debug.ico")
        self.resizable(False, False)

        self.file = None
        self.index_list: list = []
        self.length: int = 0
        self.game_cnt = -1
        self.error_cnt = 0
        self.faults = ""

        self.progressbar = Progressbar(self, orient="horizontal", length=400)
        self.label = Label(self, text="Select pgn file to test")
        self.progress = Label(self, compound="right")

        frame = Frame(self)
        self.choose_button = Button(frame, text="select file", command=self.choose_file)
        self.test_button = Button(frame, text="start test", command=self.run_test, state="disabled")
        self.test_button.pack(side="right")
        self.choose_button.pack(side="right")
        Label(frame, text="Output:").pack(side="left")

        self.output = Text(self, height=10, width=80, state="disabled", bg="light grey", font=("", 8))

        self.label.grid(row=0, column=0)
        self.progressbar.grid(row=1, column=0, pady=10, padx=3)
        self.progress.grid(row=2, column=0)
        frame.grid(row=3, column=0, sticky="we")
        self.output.grid(row=4, column=0)

        self.mainloop()

    def choose_file(self):
        """
        Επιλογή αρχείου μέσω tkinter.filedialogue.askopenfilename
        """
        self.game_cnt = -1
        self.error_cnt = 0
        self.faults = ""

        path = askopenfilename(initialdir="pgn_files", title="Choose PGN file",
                               filetypes=(("PGN files", "*.pgn"), ("All files", "*.*")))

        if path and path[-4:] == ".pgn":
            self.progressbar["value"] = 0
            self.label.config(text=path)
            self.test_button.config(state="normal")

            self.file = FilePGN(path)
            self.index_list = self.file.index_of_games
            self.length = len(self.index_list)

            self.progressbar.config(maximum=self.length)
            self.output.config(state="normal")
            self.output.delete("1.0", "end")
            self.output.config(state="disabled")
            self.progress.config(text="")

    def run_test(self):
        """
        Εκκίνηση ελέγχου
        """
        self.test_button.config(state="disabled")
        self.choose_button.config(state="disabled")
        self.game_cnt += 1

        if self.game_cnt == self.length:
            self.progress.config(text=f"finished testing {self.index_list[self.game_cnt - 1]// 2 + 1} games"
                                      f" [{self.error_cnt} error(s)]")
            self.choose_button.config(state="normal")
            self.print_results()
            return

        number = self.index_list[self.game_cnt]
        num = number // 2 + 1

        self.progressbar["value"] += 1
        self.progress.config(text=f"testing game: {num}/{self.length} [{self.error_cnt} error(s)]")

        try:
            GameLoader(list_of_moves=self.file.get_info()["moves"])
        except Exception as v:
            string = f"[{num}]: {repr(v)}"
            self.faults += ">> " + string + "\n"

            self.output.config(state="normal")
            self.output.delete("1.0", "end")
            self.output.insert(index=0.0, chars=self.faults)
            self.output.config(state="disabled")

            self.error_cnt += 1

        self.update_idletasks()
        self.after(0, self.run_test)

    def print_results(self):
        """
        Προβολή αποτελεσμάτων
        """
        res = f"games tested: {self.length}\ngames with error: {self.error_cnt}\n"
        self.output.config(state="normal")
        self.output.insert(index=0.0, chars=res)
        self.output.config(state="disabled")


if __name__ == "__main__":
    MyTest()
