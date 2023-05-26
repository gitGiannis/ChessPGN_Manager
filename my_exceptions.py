# -------------------------------------------------------------------------------------------------------------------- #
# my_exceptions.py: περιέχει προσαρμοσμένες εξαιρέσεις για χειρισμό λαθών                                              #
# -------------------------------------------------------------------------------------------------------------------- #


class PositionReached(Exception):
    """
    Δηλώνει ότι η μέθοδος game_loader.Gameloader.next_round()/game_loader.Gameloader.previous_round() έχει φτάσει στον
    πρώτο/προτελευταίο γύρο
    """
    def __init__(self):
        super().__init__()


class NoMovesFound(Exception):
    """
    Δηλώνει ότι η κλάση game_loader.Gameloader δεν κατάφερε να φορτώσει κινήσεις για τον αγώνα, διότι η συνάρτηση
    functions.get_moves_list() επέστρεψε κενή λίστα
    """
    def __init__(self):
        super().__init__()


class PossibleCorruptFile(Exception):
    """
    Δηλώνει ότι η κλάση game_loader.Gameloader δεν κατάφερε να δημιουργήσει στιγμιότυπα του αγώνα, διότι η μέθοδος
    gameplay.Gameplay.next_move() επέστρεψε None
    """
    def __init__(self):
        super().__init__()
