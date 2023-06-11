# -------------------------------------------------------------------------------------------------------------------- #
# functions.py: αρχείο για συλλογή των συναρτήσεων του προγράμματος                                                    #
# -------------------------------------------------------------------------------------------------------------------- #
from tkinter.messagebox import showinfo


# pgn.py ---------------------------------------------------------------------------------------------------------------
def get_total_rounds(game_moves: str) -> str:
    """
    Επιστρέφει τον αριθμό των γύρων του παιχνιδιού
    Λαμβάνει σαν όρισμα μία συνεχόμενη συμβολοσειρά με τις κινήσεις του αγώνα (προ επεξεργασίας) και επιστρέφει
    συμβολοσειρά με τον τελευταίο γύρο

    Ορίσματα:
    ---------
        game_moves (str): κινήσεις συγκεκριμένου αγώνα (προ επεξεργασίας)

    Επιστρεφόμενο αντικείμενο:
    --------------------------
        (str): συμβολοσειρά με τον αριθμό των γύρων του αγώνα
    """
    # βρίσκουμε την τελευταία τελεία (είναι ακριβώς μετά τον τελευταίο γύρο)
    # π.χ. ...Re7 47. Rd8 Kf6+ 48. Kd3 Re1 49. Rf8+ 1-0
    pos = game_moves.rfind(".") - 1

    # αρχικοποίηση συμβολοσειράς
    ending_rnd = ''
    # γίνεται προσπέλαση της συμβολοσειράς απο τη θέση pos...
    for char in game_moves[pos::-1]:
        # ... εώς την εύρεση κενού ή τελείας
        if char != " " and char != "\n":
            # προσθέτουμε όσους χαρακτήρες βρήκαμε (είναι οι αριθμοί του γύρου με ανάποδη σειρά)
            ending_rnd += char
        else:
            break

    try:
        # δοκιμή εάν η συμβολοσειρά μπορεί να μετατραπεί σε ακέραιο (εάν όχι έχουμε εξαίρεση)
        int(ending_rnd[::-1])
        # επιστρεφόμενη τιμή είναι συμβολοσειρά με τον αριθμό των γύρων του αγώνα
        return ending_rnd[::-1]
    except ValueError:
        return "[No Info]"


def get_moves_list(game_moves: str) -> list:
    """
    Δέχεται σαν όρισμα συμβολοσειρά με κινήσεις από το αρχείο .pgn και εξάγει τις κινήσεις σε επιστρεφόμενη λίστα
    Η λίστα περιέχει συμβολοσειρές με την κάθε κίνηση αυτούσια
    Η συνάρτηση επίσης αφαιρεί σχόλια, εάν βρεθούν

    Ορίσματα:
    ---------
        game_moves (str): κινήσεις συγκεκριμένου αγώνα (προ επεξεργασίας)

    Επιστρεφόμενο αντικείμενο:
    --------------------------
        (list): λίστα με κινήσεις (πλην τελευταίου στοιχείου που είναι το αποτέλεσμα)
    """
    if not game_moves:
        return []
    # έλεγχος εάν υπάρχουν σχόλια μέσα στις κινήσεις
    while True:
        # αναζήτηση θέσης αγκύλης αρχής σχολίου
        comment_start = game_moves.find("{")
        # εάν δε βρεθεί κάποιο σχόλιο, γίνεται έξοδος από τον ατέρμον βρόγχο
        if comment_start == -1:
            break
        # δεν έχει γίνει "break", επομένως βρέθηκε αγκύλη έναρξης σχολίου
        # οπότε γίνεται αναζήτηση θέσης αγκύλης τέλους σχολίου
        comment_end = game_moves.find("}") + 1
        # το σχόλιο αφαιρείται από τη συμβολοσειρά με τις κινήσεις
        game_moves = game_moves[:comment_start] + game_moves[comment_end:]
        # ο ατέρμον βρόγχος ξαναδιαβάζει τη νέα συμβολοσειρά για να βρει το επόμενο σχόλιο (εάν υπάρχει)

    # χωρίζουμε τις κινήσεις με βάση τα κενά και αλλαγές γραμμής
    moves_list = game_moves.split()
    # διατρέχουμε τη λίστα με τς κινήσεις
    for item in moves_list:
        # εάν η τελεία βρίσκεται μέσα στην κίνηση, σημαίνει ότι πρόκειται για δείκτη γύρου
        # και θα παραληφθεί
        if "." in item:
            # προχωράμε σε έλεγχο εάν το αρχείο pgn έχει κενό μετά το δείκτη γύρου ή όχι
            if item[-1] == ".":
                # εάν η τελεία βρίσκεται στο τέλος της συμβολοσειράς, πρόκειται για δείκτη γύρου και αφαιρείται
                # π.χ. "1."
                moves_list.remove(item)
            else:
                # επειδή η συμβολοσειρά περιέχει την τελεία "." αλλά όχι στην τελευταία θέση, έχουμε δείκτη γύρου
                # κολλητά με κάποια κίνηση (π.χ. 1.e4 αντί για 1. e4)
                # βρίσκω τη θέση όπου βρίσκεται η συμβολοσειρά με την κίνηση μέσα στη λίστα (θα χρειαστεί παρακάτω ώστε
                # να προσθέσουμε στο ίδιο σημείο την επεξεργασμένη κίνηση και να μην αλλάξουμε τη σειρά)
                index = moves_list.index(item)
                # προσωρινή αποθήκευση της κίνησης για επεξεργασία
                new_item = moves_list[index]

                # η συμβολοσειρά χωρίζεται με βάση τον χαρακτήρα της τελείας (π.χ. 1.e4 θα γίνει ["1.", "e4"])
                split_move = new_item.split(".")
                # κρατάω το δεξί μέρος της λίστας που επιστράφηκε (split_move[1] == "e4") και την εισάγω στο σωστό
                # σημείο μέσα στην αλληλουχία των κινήσεων, ώστε να μην τροποποιηθεί η σειρά
                # (αντικαθίσταται η παλιά κίνηση "1.e4" με την επεξεργασμένη "e4")
                moves_list[index] = split_move[1]

    # επιστρεφόμενη τιμή: λίστα με κινήσεις (πλην τελευταίου στοιχείου που είναι το αποτέλεσμα)
    return moves_list[:len(moves_list) - 1]


# main_program.py ------------------------------------------------------------------------------------------------------
def show_help():
    """
    Ανοίγει παράθυρο με πληροφορίες χρήσης
    """
    showinfo(title="Help",
             message="Show Files:\n"
                     "Display all pgn files from pgn_file directory\n"
                     "You can find this directory inside the app folder\n"
                     "or copy the filepath through File/Copy Path",
             detail="Select File:\nManually select a pgn file")


def about():
    """
    Ανοίγει παράθυρο με τεχνικές πληροφορίες εφαρμογής
    """
    showinfo(title="About",
             message="Chess PGN Manager v1.0\n"
                     "Release date: 14 June 2023")


def show_credits():
    """
    Ανοίγει παράθυρο με τα Credits
    """
    showinfo(title="Credits",
             message="Developers:\n"
                     ">> Moiris Ioannis\n",
             detail="Special Thanks To:\n"
                     ">> Gkogkos Christos, for the help provided")


def show_info():
    """
    Ανοίγει παράθυρο με πληροφορίες για το αρχείο pgn
    """
    showinfo(title="Info about PGN files",
             message="PGN [Portable Game Notation] is a standard plain text format\n"
                     "for recording chess games (both the moves and related data).\n"
                     "Devised around 1993 by Steven J. Edwards, pgn became\n"
                     "popular because it can be easily read by humans and is also\n"
                     "supported by most chess software\n"
                     "This application reads the information stored in a pgn file\n"
                     "and displays the basic info, as well as the development of\n"
                     "the game in a 2D environment.\n",
             detail="To do so, click the \"Show Files\" / \"Select File\" button and\n"
                     "select a pgn file to load.")
