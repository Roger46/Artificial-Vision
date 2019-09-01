import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from functools import partial
from Deteccio import deteccio
from TCPClient import enviarDades


# Classe per la finestra principal de l'App
class Ui_MainWindow(object):

    # Inicialitzacio de variables
    def __init__(self):
        self.fileName = None
        self.p1 = 1.6
        self.p2 = 180
        self.altura  = 20
        self.peces_recollir = None
        self.cercles = []

    # Declarem tots els elements de l'interficie
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Label on coloquem la nostra imatge
        self.lMarcIm = QtWidgets.QLabel(self.centralwidget)
        self.lMarcIm.setGeometry(QtCore.QRect(10, 10, 1300, 900))
        self.lMarcIm.setAutoFillBackground(False)
        self.lMarcIm.setScaledContents(True)
        self.lMarcIm.setAlignment(QtCore.Qt.AlignCenter)
        self.lMarcIm.setObjectName("lMarcIm")

        # Boto per carregar una imatge al programa
        self.bObrirIm = QtWidgets.QPushButton(self.centralwidget)
        self.bObrirIm.setGeometry(QtCore.QRect(20, 960, 111, 31))
        self.bObrirIm.setObjectName("bObrirIm")
        self.bObrirIm.clicked.connect(self.obrirDialegImatge)

        # Boto per ampliar la imatge carregada
        self.bAmpliarIm = QtWidgets.QPushButton(self.centralwidget)
        self.bAmpliarIm.setGeometry(QtCore.QRect(150, 960, 121, 31))
        self.bAmpliarIm.setObjectName("bAmpliarIm")
        self.bAmpliarIm.clicked.connect(self.ampliarImatge)

        # Etiqueta per el primer parametre que pot modificar l'usuari
        self.lParam1 = QtWidgets.QLabel(self.centralwidget)
        self.lParam1.setGeometry(QtCore.QRect(1430, 190, 211, 16))
        self.lParam1.setObjectName("lParam1")

        # Entrada de text per on rebem el valor que vol l'usuari
        self.InParam1 = QtWidgets.QTextEdit(self.centralwidget)
        self.InParam1.setGeometry(QtCore.QRect(1430, 220, 101, 41))
        self.InParam1.setObjectName("InParam1")

        # Boto per modificar el parametre
        self.bParam1 = QtWidgets.QPushButton(self.centralwidget)
        self.bParam1.setGeometry(QtCore.QRect(1550, 220, 71, 41))
        self.bParam1.setObjectName("bParam1")
        self.bParam1.clicked.connect(partial(self.modificar_param, 1))

        # Boto que obre una finstra emergent amb una petita explicacio del parametre
        self.bInfoParam1 = QtWidgets.QPushButton(self.centralwidget)
        self.bInfoParam1.setGeometry(QtCore.QRect(1640, 220, 31, 41))
        self.bInfoParam1.setObjectName("bInfoParam1")
        self.bInfoParam1.clicked.connect(partial(self.popup_informacio, 1))

        # Etiqueta per el segon parametre que pot modificar l'usuari
        self.lParam2 = QtWidgets.QLabel(self.centralwidget)
        self.lParam2.setGeometry(QtCore.QRect(1430, 290, 211, 16))
        self.lParam2.setObjectName("lParam2")

        # Entrada per el segon parametre modificable
        self.InParam2 = QtWidgets.QTextEdit(self.centralwidget)
        self.InParam2.setGeometry(QtCore.QRect(1430, 320, 101, 41))
        self.InParam2.setObjectName("InParam2")

        # Boto per modifcar el segon parametre
        self.bParam2 = QtWidgets.QPushButton(self.centralwidget)
        self.bParam2.setGeometry(QtCore.QRect(1550, 320, 71, 41))
        self.bParam2.setObjectName("bParam2")
        self.bParam2.clicked.connect(partial(self.modificar_param, 2))

        # Boto per rebre informacio del segon parametre
        self.bInfoParam2 = QtWidgets.QPushButton(self.centralwidget)
        self.bInfoParam2.setGeometry(QtCore.QRect(1640, 320, 31, 41))
        self.bInfoParam2.setObjectName("bInfoParam2")
        self.bInfoParam2.clicked.connect(partial(self.popup_informacio, 2))

        # Boto per processar l'imatge
        self.bCalcular = QtWidgets.QPushButton(self.centralwidget)
        self.bCalcular.setGeometry(QtCore.QRect(1470, 420, 161, 51))
        self.bCalcular.setObjectName("bCalcular")
        self.bCalcular.clicked.connect(self.processar_imatge)

        # Etiqueta de seleccio de objectes reconeguts
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(1430, 620, 241, 21))
        self.label.setObjectName("label")

        # Entrada de text per on l'usuari indica quins objectes vols recollir
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(1430, 650, 171, 41))
        self.textEdit.setObjectName("textEdit")

        # Boto per obtenir les peces
        self.bRecollir = QtWidgets.QPushButton(self.centralwidget)
        self.bRecollir.setGeometry(QtCore.QRect(1610, 650, 51, 41))
        self.bRecollir.setObjectName("bRecollir")
        self.bRecollir.clicked.connect(self.obtenir_peces)

        # Boto per enviar les coordenades al robot
        self.bEnvia = QtWidgets.QPushButton(self.centralwidget)
        self.bEnvia.setGeometry(QtCore.QRect(1480, 760, 131, 51))
        self.bEnvia.setObjectName("bEnvia")
        self.bEnvia.clicked.connect(self.enviar_coordenades)


        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    ################################################################
    #                       Bloc de Funcions                       #
    ################################################################

    # Metode per obrir el selecctor de fitxers 
    def obrirDialegImatge(self):
        # Obrim la finestra de dialeg i obtenim el nom
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        self.fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
                        None,
                        "QFileDialog.getOpenFileName()",
                        "",
                        "All Files (*);;Python Files (*.py)",
                        options=options)


        # Posem l'imatge on toca del Layout
        self.lMarcIm.setPixmap(QtGui.QPixmap(self.fileName))

    # Metode per ampliar la imatge que s'ha obert
    def ampliarImatge(self):
        #Comprovem que hi ha una imatge seleccionada
        if self.fileName != None:
            print("Imatge en gran")
            self.openSecondWindow()

        else: 
            self.popup_error(1)

    # Metode que obre la segona imatge amb una finestra a part
    def openSecondWindow(self):
        self.secondWindow = QtWidgets.QMainWindow()
        self.ui = Ui_SecondWindow()
        self.ui.setupUi(self.secondWindow)
        self.ui.label.setPixmap(QtGui.QPixmap(self.fileName))        
        self.ui.label.adjustSize()
        self.secondWindow.show()

    # Metode per indicar un error en el programa
    def popup_error(self, boto):
        msg = QMessageBox()
        msg.setWindowTitle("Alerta!")
        if boto == 1:
            msg.setText("No hi ha cap imatge carregada")
        elif boto == 2:
            msg.setText("No s'ha detectat cap peça")
        elif boto == 3:
            msg.setText("No s'ha seleccionat cap peça per recollir")
        else:
            msg.setText("No s'ha processat cap imatge")
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()

    # Metode per donar mes informacio a l usuairi sobre els parametres que modifica
    def popup_informacio(self, boto):
        if boto == 1:
            msg = QMessageBox()
            msg.setWindowTitle("Informacio Param 1")
            msg.setText("Amb aquest parametre es pot modificar x")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()
        else: 
            msg = QMessageBox()
            msg.setWindowTitle("Informacio Param 2")
            msg.setText("Aquest parametre defineix la distància minima entre els centres detectats. A menys d'aquesta distància no buscara cap centre. La seva unitat son pixels")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()

    # Metode per obtenir els valors dels parametres que ha entrat l'usuari
    def modificar_param(self, boto):
        if boto == 1:
            self.p1 = self.InParam1.toPlainText()
        else:
            self.p2 = self.InParam2.toPlainText()

    # Metode per processar l'imatge
    def processar_imatge(self):
        status, self.imNova, self.cercles = deteccio(self.fileName, self.p1, self.p2)
        if status == 0:
            print("S'han trobat peces")
            # Tot correcte, carregem la imatge nova
            self.lMarcIm.setPixmap(QtGui.QPixmap(self.imNova))
            # Substituim el filename ja que ara l'imatge es un altre diferent
            self.fileName = self.imNova
            #print(self.imNova)
        elif status == 1:
            print("No hi ha cercles")
            self.popup_error(2)

    # Metode per enviar les coordenades al robot
    def enviar_coordenades(self):
        print("Enviant Coordenades")
        # Recuperar les peces que l'usuari vol enviar (Warning si no en te cap introduida)
        if (self.peces_recollir == None):
            self.popup_error(3)
        # comprovem si s'ha processat l'imatge mirant si el vector de cercles te valors dins
        elif (len(self.cercles) == 0):
            self.popup_error(4)
        else:
            # obtenim una llista d'strings amb els valors de les peces que volem recollir
            peces_usuari = self.peces_recollir.split(',')
            # transformem la llista d'strings a llista de enters per quedarnos amb els indexs
            idx_peces = list(map(int, peces_usuari))
            message = str(len(idx_peces)) + "/" # Acumularem les coordenades de les peces en aquesta variable
            for idx in idx_peces:
                cercle = self.cercles[idx]
                # Obtenim X i Y en coordenades de la camera
                xc = cercle[0]
                yc = cercle[1]
                # Tranformarlos a mm (10mm = 40px)
                # Els transformem a coordenades de robot
                xc_aux = xc + 143 # Afegim el desplaçament fins al nostre centre
                yc_aux = yc + 46
                xr_aux = (xc_aux*10)/40 # Regla de 3
                yr_aux = (yc_aux*10)/40
                ###### Enviar xr, yr i altura al robot
                xr = int(round(xr_aux))
                yr = int(round(yr_aux))
                message = message + str(xr) + ";" + str(yr) + ";" + "48/"
                print(message)
            enviarDades(message) # Enviem el conjunt de punts
                 

    def obtenir_peces(self):
        self.peces_recollir = self.textEdit.toPlainText()

    # Metode que dona el text que volem a totes les labels de l'interficie
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Image Processing APP"))
        self.lMarcIm.setText(_translate("MainWindow", "Obrir Imatge Aqui"))
        self.bObrirIm.setText(_translate("MainWindow", "Obrir Imatge"))
        self.bAmpliarIm.setText(_translate("MainWindow", "Ampliar"))
        self.lParam1.setText(_translate("MainWindow", "Entra valor per parametre 1 (Per defecte 1.6):"))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lParam1.setFont(font)
        self.lParam1.adjustSize()
        self.bParam1.setText(_translate("MainWindow", "Ok"))
        self.bInfoParam1.setText(_translate("MainWindow", "?"))
        self.lParam2.setText(_translate("MainWindow", "Entra valor per parametre 2 (Per defecte 180):"))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lParam2.setFont(font)
        self.lParam2.adjustSize()
        self.bParam2.setText(_translate("MainWindow", "OK"))
        self.bInfoParam2.setText(_translate("MainWindow", "?"))
        self.label.setText(_translate("MainWindow", "Indica peces a recollir: (Separades per ,)"))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.adjustSize()
        self.bRecollir.setText(_translate("MainWindow", "Ok"))
        self.bEnvia.setText(_translate("MainWindow", "Envia"))
        self.bCalcular.setText(_translate("MainWindow", "Processar"))


################################################################
#              Interficie segona pantalla                      #
################################################################

# Classe per la finestra secundaria de l'App
class Ui_SecondWindow(object):
    def setupUi(self, SecondWindow):
        SecondWindow.setObjectName("SecondWindow")
        SecondWindow.resize(530, 389)
        self.centralwidget = QtWidgets.QWidget(SecondWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setEnabled(True)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 516, 375))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label.setText("")
        self.label.setScaledContents(False)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)
        SecondWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(SecondWindow)
        QtCore.QMetaObject.connectSlotsByName(SecondWindow)

    def retranslateUi(self, SecondWindow):
        _translate = QtCore.QCoreApplication.translate
        SecondWindow.setWindowTitle(_translate("SecondWindow", "MainWindow"))



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    # Tanquem l'interficie
    sys.exit(app.exec_())
