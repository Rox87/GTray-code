
from PyQt5.QtWidgets import QDesktopWidget,QCheckBox,QLineEdit,QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPixmap,QDesktopServices,QIcon
from services.klisten import KListen
from handler import Gtray
import configparser
from pessoal.Escriba import registrador
import os
import subprocess
import sys
from dotenv import load_dotenv

load_dotenv()

r = registrador()
r.addHand()
logger = r.get_logger()
# Create a new config parser object
config = configparser.ConfigParser()

# Read in the configuration file
config.read('assets/config.ini',encoding='utf-8')


class GTray_CFG_UI(QWidget):

    def __init__(self):
        super().__init__()

        self.gt = None
        self.kl = None
        self.visible = None
        self.autostart = False
        self.fake_event = None
        self.lbl_shortcut_text = None
        self.button_get_shortcut_clicked = False
        self.index=0
        self.initUI()
    def pos_left(self):
            qr = self.frameGeometry()
            cp = QDesktopWidget().availableGeometry().topLeft()
            qr.moveCenter(cp)
            self.move(qr.center())
    def initUI(self):
        self.header_title = QLabel(config['GTRAY']['header_title'])
        self.header_title.setStyleSheet('''font-size: 48px;background-color:purple''')

        self.image = QLabel()
        self.pixmap = QPixmap(config['GTRAY']['favicon'])
        self.pixmap = self.pixmap.scaled(300, 300)
        self.image.setPixmap(self.pixmap)
        self.image.mousePressEvent = self.input_blockunblock
        self.header_apikey = QLabel(config['GTRAY']['header_apikey_text'])
        self.header_apikey.setStyleSheet('''color:white; font-size: 25px;background-color:#191970;''')
        self.input_apikey = QLineEdit()
        self.input_apikey_state = config['GTRAY']['input_apikey_state']

        self.btn_apikey = QPushButton(config['GTRAY']['btn_apikey_block_text'])

    
    

        self.input_blockunblock(self.fake_event)

        self.lbl_shortcut = QLabel()
        self.header_shortcut = QLabel(config['GTRAY']['header_shortcut_text'])
        self.btn_shortcut = QPushButton(config['GTRAY']['btn_shortcut_text'])
        self.btn_shortcut.clicked.connect(self.get_listen_dialog)
        self.header_shortcut.setStyleSheet('''color:white; font-size: 25px;background-color:#191970;''')
        self.lbl_shortcut.setStyleSheet('''color:black;font-size: 20px; background-color:lightgrey;''')
        self.setStyleSheet("""
    background-color: #2B5DD1;
    color: #FFFFFF;
    border-style: outset;
    padding: 2px;
    font: bold 20px;
    border-width: 6px;
    border-radius: 25px;
    border-color: #2752B8;
    width:200px;
    }
    QPushButton {
    border-radius: 5px;
    border: 1px solid #000;
    padding: 10px 20px;
    background: darkred;

    font-size: 2em;
    }
    QPushButton:hover {
        color:white;
        background-color: #D2691E;
                }
            """)
        
        self.checkbox_visibility = QCheckBox("Visível")
        self.checkbox_visibility.setChecked(True)
        self.checkbox_visibility.stateChanged.connect(self.checkbox_visibility_changed)

        self.header_startstop = QLabel(config['GTRAY']['header_startstop_text'])
        self.header_startstop.setStyleSheet('''color:white; font-size: 25px;background-color:#191970;''')
        self.btn_startstop = QPushButton(config['GTRAY']['btn_startstop_text'])
        self.btn_startstop.setStyleSheet('''QPushButton {
            color:white; background-color:green;
            }
                QPushButton:hover {
        color:white;
        background-color: darkgreen;
                }
            ''')
        self.btn_startstop.clicked.connect(self.startstop)

        self.get_shortcut()

        # Adiciona o QLabel ao layout
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.header_title)
        self.vbox.addWidget(self.image)
        self.vbox.addWidget(self.header_apikey)
        self.vbox.addWidget(self.input_apikey)
        self.vbox.addWidget(self.btn_apikey)
        self.vbox.addWidget(self.header_shortcut)
        self.vbox.addWidget(self.lbl_shortcut)
        self.vbox.addWidget(self.btn_shortcut)  
        self.vbox.addWidget(self.header_startstop)
        self.vbox.addWidget(self.checkbox_visibility)
        self.vbox.addWidget(self.btn_startstop)

        self.image.setAlignment(Qt.AlignCenter)
        self.header_title.setAlignment(Qt.AlignCenter)
        self.header_apikey.setAlignment(Qt.AlignCenter)
        self.input_apikey.setAlignment(Qt.AlignCenter)
        self.lbl_shortcut.setAlignment(Qt.AlignCenter)
        self.header_shortcut.setAlignment(Qt.AlignCenter)
        self.header_startstop.setAlignment(Qt.AlignCenter)
        self.setLayout(self.vbox)
        
        
        self.setGeometry(400, 400, 400, 200)
        self.setWindowTitle('GTray')
        self.setWindowOpacity(0.9)
           
        self.setWindowIcon(QIcon(config['GTRAY']['favicon']))
        self.pos_left()
        self.show()
    def start_buttons_def(self):
        self.btn_startstop.setText('Iniciar')
        self.btn_startstop.setStyleSheet('''
        QPushButton {
        color:white; background-color:green;
        }
            QPushButton:hover {
    color:white;
    background-color: darkgreen;
            }
        ''')
        
    def stop_buttons_def(self):
        self.btn_startstop.setText('Pausar')
        self.btn_startstop.setStyleSheet('''
        QPushButton {
        color:white; background-color:darkred;
        }
            QPushButton:hover {
    color:white;
    background-color: #D2691E;
            }
        ''')

    def checkbox_visibility_changed(self, state):
        if state != 2:
            self.visible=False
            self.start_buttons_def()
        else:
            self.visible=True

    def startstop(self):
        if not hasattr(self.gt,'UI'):
            self.gt = Gtray(self,logger)
            self.apikey = os.getenv("OPENAI_API_KEY")
            self.gt.change_key(self.apikey)
            

        if self.visible==False:
            self.gt.hide_terminal()
            self.visible=True
            self.autostart = True
        elif self.visible==True:
            self.gt.show_terminal()
            self.visible=False

        if self.autostart == True:
            self.stop_buttons_def()
            self.gt.start()
            self.autostart = False
            self.gt.run()
            print('saindo...')
        else:
            self.start_buttons_def()
            self.gt.stop()
            #self.gt.on_exit()
            del self.gt
            self.gt = None
            self.autostart = True


        
    def input_blockunblock(self,event=None):
        if self.input_apikey_state != 'unblock':
            self.btn_apikey.setText(config['GTRAY']['btn_apikey_block_text'])
            self.btn_apikey.disconnect()
            self.btn_apikey.clicked.connect(self.sobre_apikey)
            self.input_apikey.setText(config['GTRAY']['input_apikey_bloqueado'])
            self.input_apikey.setEnabled(False)
            self.input_apikey.setStyleSheet('''color:black; font-size: 19px;background-color:lightgrey;''')
            self.input_apikey_state = 'unblock'
        else:
            self.apikey = os.getenv("OPENAI_API_KEY")
            if self.gt == None:
                self.gt = Gtray(self,logger)
            self.gt.change_key(self.apikey)
            self.btn_apikey.setText(config['GTRAY']['btn_apikey_text'])
            try:
                self.btn_apikey.disconnect()
            except:
                pass
            self.btn_apikey.clicked.connect(self.write_k)
            self.input_apikey.setText(self.apikey)
            self.input_apikey.setEnabled(True)
            self.input_apikey.setFocus()
            self.input_apikey.setStyleSheet('''color:black; font-size: 25px;background-color:white;''')
            self.input_apikey_state = 'block'

    def write_k(self):
        try:
            with open(config['GPT']['k'],'w') as f:
                f.write(self.input_apikey.text())
        except Exception as ex:
            print(ex)
        QMessageBox.information(self, config['GTRAY']['write_k_0'],config['GTRAY']['write_k_1'], QMessageBox.Ok)
        self.input_apikey_state = 'block'
        self.input_blockunblock()

    def sobre_apikey(self):
        
        about = QMessageBox.question(self, config['GTRAY']['sobre_apikey_0'],config['GTRAY']['sobre_apikey_1'], QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if about == QMessageBox.Yes:
            url = QUrl('https://platform.openai.com/account/api-keys')
            QDesktopServices.openUrl(url)
        else:
            pass
        QMessageBox.information(self, config['GTRAY']['sobre_apikey_0'],config['GTRAY']['sobre_apikey_2'], QMessageBox.Ok)

    def get_listen_dialog(self):
        shortcut = QMessageBox.question(self, config['GTRAY']['sobre_shortcut_0'],config['GTRAY']['sobre_shortcut_1'], QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if shortcut == QMessageBox.Yes:
            self.listen_shortcut()
        else:
            pass
     
    def get_shortcut(self):
        try:
            with open(config['GTRAY']['shortcut_file'],'r') as f:
                self.shortcut = f.read()
        except Exception as ex:
            print(ex)
        
        # Single update for both labels
        self.lbl_shortcut.setText(f"{self.shortcut}")
        self.header_shortcut.setText(config['GTRAY']['header_shortcut_text'])
        QApplication.processEvents()
  


    def listen_shortcut(self):
        self.button_get_shortcut_clicked = True        
        self.header_shortcut.setText(config['GTRAY']['header_shortcut_state_rec'])
        self.header_shortcut.setStyleSheet('font-size=20px')
        self.lbl_shortcut.setText(config['GTRAY']['lbl_shortcut_state_rec'])
        # Single batch update for UI elements
        QApplication.processEvents()
        # Single call to handle shortcut
        self.listen()
        self.get_shortcut()
        self.autostart = False

    def listen(self):
        if hasattr(self.kl, 'kl'):
            self.kl.__init__()
        else:
            self.kl = KListen()
        self.get_shortcut()

        self.kl.run()
        self.header_shortcut.setStyleSheet('''color:white; font-size: 25px;background-color:#191970;''')
        self.kl.set_activated(False)
        print('shortcut capturado')
    
    def closeEvent(self, event):
        self.gt.on_exit()
        event.accept()

    def hide_UI(self):
       print('app no plano de fundo')
       self.hide()
       #self.the_program_to_hide = win32gui.GetForegroundWindow()
       #win32gui.ShowWindow(self.the_program_to_hide , win32con.SW_HIDE)

    def show_UI(self):
       print('app visivel')
       self.show()
       #self.the_program_to_hide = win32gui.GetForegroundWindow()
       #win32gui.ShowWindow(self.the_program_to_hide , win32con.SW_HIDE)
    def cmd_start(self):
        self.startstop()



if __name__ == '__main__':
        pid = os.getpid()
        # Abre (ou cria) um arquivo no modo de escrita ('w')
        with open('cmd/lastpid.txt', 'r') as file:
            pid2 = file.read()
        CREATE_NO_WINDOW = 0x08000000
        subprocess.call(f'taskkill /f /FI "PID eq {pid2}"', creationflags=CREATE_NO_WINDOW)
        
        with open('cmd/lastpid.txt', 'w') as file:
            file.write(f'{pid}')

        app = QApplication(sys.argv)
        ex = GTray_CFG_UI()
        try:
            if sys.argv[1] == "1": 
                logger.info(f'main > {sys.argv[1]}')           
                ex.visible=True
                ex.autostart=True
                ex.startstop()
                sys.exit(app.exec_())
            elif sys.argv[1] == "2":
                logger.info(f'main > {sys.argv[1]}')
                ex.visible=False
                ex.autostart=True
                ex.startstop()
                ex.gt.run()
            else:
                raise Exception
        except:
                logger.info(f'main > UI')
                ex.visible=True
                ex.autostart=False
                ex.startstop()
                sys.exit(app.exec_())
        sys.exit(0)


