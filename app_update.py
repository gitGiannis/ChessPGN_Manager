# -------------------------------------------------------------------------------------------------------------------- #
# update_app.py: περιέχει την κλάση AppUpdate                                                                          #
# -------------------------------------------------------------------------------------------------------------------- #
from os.path import abspath


class AppUpdate:
    """
    Ενημερώνει την εφαρμογή
    """
    def __init__(self):
        app_dir = abspath("main.py")
        print(app_dir)


if __name__ == "__main__":
    AppUpdate()