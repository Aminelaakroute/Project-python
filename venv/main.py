import sys , res
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow,QPushButton, QApplication
import sqlite3


class LoginDialog(QMainWindow):
    def __init__(self):
        super(LoginDialog, self).__init__()
        loadUi('interfacelogin.ui', self)
        password = self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login_button.clicked.connect(self.loginfunction)



    def loginfunction(self):
        email = self.email.text()
        password = self.password.text()
        if len(email) == 0 or len(password) == 0:
            self.error.setText("Please input all fields")
        else:
            conn = sqlite3.connect("login.db")
            cur = conn.cursor()
            query = 'SELECT password FROM login WHERE email =\'' + email + "\'"
            cur.execute(query)
            result_pass = cur.fetchone()
            if result_pass is not None:
                password_from_db = result_pass[0]
                if password_from_db == password:
                    print("Successfully logged in.")
                    self.showHomePage()
                    self.error.setText("")
                else:
                    self.error.setText("Invalid password")
            else:
                self.error.setText("User not found")

    def showHomePage(self):
        #Charger la page d'accueil après la connexion réussie
        loadUi('page1.ui', self)
        #Connecter le bouton de déconnexion à la fonction log_out
        self.button_logout.clicked.connect(self.log_out)
        #Connecter les autres boutons aux fonctions correspondantes
        self.Books_2.clicked.connect(self.showPage1)
        self.Client.clicked.connect(self.showPage2)
        self.Management_2.clicked.connect(self.showPage3)



    def showPage1(self):
        self.stackedWidget.setCurrentIndex(0)

        self.loadData1()
    def showPage2(self):
        self.stackedWidget.setCurrentIndex(0)

        self.loadData2()
    def showPage3(self):
        self.stackedWidget.setCurrentIndex(0)

        self.loadData3()



    #_____________________________________________
    def loadData1(self):

        Data1 = [{"Book Title":"The Catcher in the Rye","Book Author": "J.D. Salinger","Book ID" :"978-0-316-76948-0","Is Available": True},
                 {"Book Title":"To Kill a Mockingbird","Book Author": "Harper Lee","Book ID" : "978-0-06-112008-4","Is Available": True},
                 {"Book Title":"1984-15ff4","Book Author": "George Orwell","Book ID" : "978-0-452-28423-4","Is Available": True},
                 {"Book Title":"The Catcher ","Book Author": "Salinger","Book ID" : "97876948-0","Is Available": False},
                 {"Book Title":"Mockingbird","Book Author": "Lee","Book ID" : "978-0-8-4","Is Available": True},
                 {"Book Title":"1984","Book Author": " Orwell","Book ID" : "978-28423-4","Is Available": True}
                 ]
        self.loadData(Data1,0)


    def loadData2(self):

        Data2 = [
            {"First Name": "amine",
             "Last Name": "4555",
             "Client ID": "112055213",
             "Client Email": "laa.amine12@gmail.com"
            }
            ]
        self.loadData(Data2, 0)
    def loadData3(self):

        Data3 = [
            {"Client Name": "amine",
             "Client ID": "112055213",
             "Books Borrowed": "1984-15ff4"
            }
            ]
        self.loadData(Data3, 0)


    def loadData(self, data, pageIndex):
        if not data:
            return

        # Réinitialiser le tableau à chaque fois que des données sont chargées
        self.tableWidget.clear()

        row = 0
        col_names = list(data[0].keys())  # Utiliser les noms de colonnes de la première ligne comme référence

        # Configurer les colonnes du tableau
        self.tableWidget.setColumnCount(len(col_names))
        self.tableWidget.setHorizontalHeaderLabels(col_names)

        self.tableWidget.setRowCount(len(data))
        for item in data:
            col = 0
            for key in col_names:
                self.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(str(item.get(key, ''))))
                col += 1
            row += 1

        # Définir la page actuelle après avoir configuré les widgets
        self.stackedWidget.setCurrentIndex(pageIndex)

    def log_out(self):
        # Revenir à la page de connexion
        loadUi('interfacelogin.ui', self)

        # Créer une nouvelle instance de LoginDialog
        new_instance = LoginDialog()

        # Connecter à nouveau le bouton de connexion après la déconnexion
        self.login_button.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)

        # Afficher la nouvelle instance
        new_instance.show()

def main():
    app = QApplication(sys.argv)
    mainwindow = LoginDialog()
    mainwindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()







