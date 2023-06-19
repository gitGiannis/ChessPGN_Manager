# -------------------------------------------------------------------------------------------------------------------- #
# manual_game_selector.py: περιέχει την κλάση ManualGameSelector                                                       #
# -------------------------------------------------------------------------------------------------------------------- #
from tkinter import Frame, Button, Listbox, Scrollbar, Label
from game_loader import GameLoader
from gui import GUI
from pgn import FilePGN


class ManualGameSelector(Frame):
    """
    Ανοίγει ένα παράθυρο εξερεύνησης των windows
    Σε αυτό το παράθυρο ο χρήστης επιλέγει χειροκίνητα ένα συγκεκριμένο αρχείο pgn το οποίο θέλει να φορτώσει
    Εάν επιλεχθεί έγκυρο filepath προς αρχείο με κατάληξη pgn, κατασκευάζει ένα νέο frame στο κύριο παράθυρο και
    τοποθετεί σε αυτό listbox με τα περιεχόμενα παιχνίδια
    Από αυτά, ο χρήστης μπορεί να επιλέξει και να τρέξει όποιο επιθυμεί
    Κληρονομεί από την κλάση tkinter.Frame

    Ορίσματα:
    ---------
        root (main_program.MainProgram):
            κύριο παράθυρο της εφαρμογής

        pgn_filepath (str):
            διεύθυνση αρχείου pgn που επιλέχθηκε

    Μέθοδοι:
    --------
        display_game():
            προβολή του παιχνιδιού που επιλέχθηκε

        retrieve_master():
            επαναφορά κύριου πλαισίου
    """
    def __init__(self, root, pgn_filepath: str):
        # κλήση της super() για αρχικοποίηση γονικής κλάσης
        super().__init__()
        # ορισμός master του frame
        self.root = root
        # ενεργοποίηση επιλογής "back" στο μενού μπάρας
        self.root.file_menu.entryconfig(5, state="normal", command=self.retrieve_master)

        # αρχικοποίηση αντικειμένων που θα χρειαστούν ------------------------------------------------------------------
        file = FilePGN(pgn_filepath)
        self.file_path = pgn_filepath
        self.warning_label = Label(self,
                                   bg="light blue",
                                   fg="red",
                                   font=("consolas", 10, "bold"),
                                   pady=5)

        # αρχικοποίηση listbox που θα περιέχει τα παιχνίδια που διαβάστηκαν από το αρχείο pgn --------------------------
        self.listbox = Listbox(self, bg="#f7ffde", width=80, height=20, font=("consolas", 10))

        # προσθήκη μπάρας κύλισης στο listbox
        scrollbar = Scrollbar(master=self, command=self.listbox.yview)
        self.listbox.config(yscrollcommand=scrollbar.set)

        # αρχικοποίηση κουμπιών ----------------------------------------------------------------------------------------
        self.button_run = Button(self,
                                 text="Run",
                                 font=("consolas", 12, "bold"),
                                 background="light green",
                                 activebackground="green",
                                 width=12,
                                 command=self.display_game)

        self.button_back = Button(self,
                                  text="Back",
                                  font=("consolas", 12, "bold"),
                                  background="light green",
                                  activebackground="green",
                                  width=12,
                                  command=self.retrieve_master)

        # τοποθέτηση στο παράθυρο --------------------------------------------------------------------------------------
        self.listbox.grid(row=0, column=0, sticky="ne")
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.button_back.grid(row=1, column=0, sticky="w")
        self.button_run.grid(row=1, column=0, columnspan=2, sticky="e")

        # προσθήκη πλαισίου στο κυρίως παράθυρο ------------------------------------------------------------------------
        self.config(bg="light blue")
        self.pack()

        # φόρτωση πληροφοριών που θα προβληθούν στο listbox ------------------------------------------------------------
        # δημιουργία πίνακα για συλλογή των game_dictionaries κάθε παιχνιδιού
        self.game_dict_collection = []
        # προσθήκη παιχνιδιών που διαβάστηκαν, στο listbox
        for i, num in enumerate(file.get_index_of_games()):
            # δημιουργία του λεξικού με τη μέθοδο get_info της κλάσης FilePGN
            game_dictionary = file.get_info(num)
            # προσθήκη του λεξικού στη συλλογή με τα λεξικά του συγκεκριμένου αρχείου pgn
            self.game_dict_collection.append(game_dictionary)
            self.listbox.insert(i, f'{str(i + 1) + ".":4}{game_dictionary["White"]} vs '
                                   f'{game_dictionary["Black"]} '
                                   f'({game_dictionary["Result"]})')
            # εμφάνιση αποτελεσμάτων ανα εκατό, για ανανέωση του παραθύρου εάν έχουμε πολλά αρχεία
            if i % 100 == 0:
                self.update()

    def display_game(self):
        """
        Προβολή του παιχνιδιού που επιλέχθηκε
        """
        # αποθηκεύουμε τις πληροφορίες της επιλογής του χρήστη από το listbox
        index = self.listbox.curselection()
        # εάν επιλέξει κάτι...
        if index:
            # κρατάμε το πρώτο κομμάτι του επιστρεφόμενου tuple (0, 1, 2 κλπ)
            # και το πολλαπλασιάζουμε με το 2 ώστε να αντιστοιχεί σε κάποιο παιχνίδι από τη λίστα
            # (βλ. pgn.py μέθοδος spilt_files)
            index_for_games = index[0] * 2
            # κρατάμε το πρώτο κομμάτι του επιστρεφόμενου tuple ως έχει για τις πληροφορίες του αγώνα
            index_for_collection = index[0]
            try:
                # συλλογή των στιγμιοτύπων του παιχνιδιού μέσω της κλάσης GameLoader
                game_loader = GameLoader(self.file_path, index_for_games)
                # τρέχουμε το GUI (γραφική αναπαράσταση παιχνιδιού) με το συγκεκριμένο παιχνίδι
                GUI(game_loader, self.game_dict_collection[index_for_collection])
            except Exception as v:
                self.warning_label.config(text=str(v))
                self.warning_label.grid(row=1, column=0, columnspan=2, sticky="n")
                self.warning_label.after(3000, self.warning_label.grid_forget)
        else:
            # εμφάνιση μηνύματος σφάλματος σε περίπτωση που δεν έχει γίνει επιλογή
            self.warning_label.config(text="Select a game to continue")
            self.warning_label.grid(row=1, column=0, columnspan=2, sticky="n")
            self.warning_label.after(3000, self.warning_label.grid_forget)

    def retrieve_master(self):
        """
        Επαναφορά κύριου πλαισίου
        """
        # επαναφορά κύριου πλαισίου
        self.root.main_frame.pack()
        # επαναφορά μενού
        self.root.file_menu.entryconfig(0, state="normal")
        self.root.file_menu.entryconfig(1, state="normal")
        self.root.file_menu.entryconfig(3, state="normal")
        self.root.file_menu.entryconfig(5, state="disabled")
        # τερματισμός τρέχοντος frame
        self.destroy()
