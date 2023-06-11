# -------------------------------------------------------------------------------------------------------------------- #
# _installer.py: περιέχει τη συνάρτηση install_app για εγκατάσταση εφαρμογής                                           #
# -------------------------------------------------------------------------------------------------------------------- #
import zipfile


def install_app():
    """
    Πραγματοποιεί εγκατάσταση της εφαρμογής κάνοντας αποσυμπίεση των αρχείων
    python -m PyInstaller --onefile --name="Install Wizard" _installer.py
    """
    print("Install Wizard for Chess PGN manager v1.0")
    input("press <enter> to continue...")
    # δημιουργία λίστας αρχείων
    files = ["PGN_Manager_1.zip", "PGN_Manager_2.zip", "PGN_Manager_3.zip"]
    for path in files:
        try:
            # αποσυμπίεση αρχείου
            with zipfile.ZipFile(path, 'r') as zip_ref:
                print("extracting " + path, end='')
                zip_ref.extractall()
                print(" [done]")
        except:
            print("failed to install app!\n"
                  "make sure the install wizard is in the same directory\n"
                  "as the three zip files (PGN_Manager_1, ...2 and ...3)")
            break
    else:
        # μήνυμα επιτυχούς εγκατάστασης
        print("app installed successfully!\n"
              "you can run it by double clicking PGN_Manager.exe\n"
              "in the 'PGN_Manager' directory")

    input("\n\npress <enter> to continue...")


if __name__ == "__main__":
    install_app()
