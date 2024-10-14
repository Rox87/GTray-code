import pystray
from PIL import Image
import win32gui,win32con
import keyboard
from pessoal.Decorador import tempo_decorrido
from pessoal.IA import IA
from pessoal.Engineer import Engineer

import configparser
# Create a new config parser object
config = configparser.ConfigParser()

# Read in the configuration file
config.read('assets/config.ini',encoding='utf-8')


class Gtray:
    processo = None
    icon = None
    shortcut = None
    
    def __init__(self,UI=None,logger_from=None):
        global logger
        logger = logger_from
        self.Engineer = Engineer(logger_from)
        self.AI = None
        self.UI = UI
        logger.info('preparando...')
        self.sair = False
        # força aplicação continuar executando mesmo em caso de erro
        self.prosseguir = True     
        # prompt que permite esconder/mostrar o terminal
        self.the_program_to_hide = win32gui.GetForegroundWindow()
        
        self.mode = None

        # icons
        logger.info('carregando icones')
        self.red_image = Image.open(config['GTRAY']['gtON'])
        #self.green_image = Image.open(config['GTRAY']['gtOFF'])
        
        # Itens do menu que será construido dinamicamente
        logger.info('preparando menu')
        #self.menu_state = pystray.MenuItem("Pausar",self.UI.startstop)
        self.menu_visible = pystray.MenuItem("Mostrar UI",self.show_terminal)
        self.menu_exit = pystray.MenuItem("Sair", self.on_exit)

        # Define o obj do Gtray
        self.icon = pystray.Icon("GPTray", self.red_image, menu=pystray.Menu())
        
        # Esconde o terminal por padrão
        #logger.info('escondendo o terminal')
        #self.hide_terminal()
        
        # Incia app funcionando
        #self.start()

    def ignorar(self):
         logger.info('GPTray esta pausado')

    def start(self):
        with open(config['GTRAY']['shortcut_file'],'r') as f:
             self.shortcut = f.read()
        try:
            with open(config['GTRAY']['shortcut_py_file'],'r') as f:
                self.shortcut_py = f.read()
        except:
             self.shortcut_py="F9"

    
        logger.info(f'chatGPT > contato salvo nos favoritos ({self.shortcut})')
        keyboard.add_hotkey(f'{self.shortcut.lower()}', self.chat_handler)
        keyboard.add_hotkey(f'{self.shortcut_py.lower()}', self.python_handler)
        logger.info(f'precione {self.shortcut} com um texto selecionado em um campo editavel e aguarde...')
            

        #self.menu_state = pystray.MenuItem("Pausar", self.stop)
        #self.build_menu()
        #self.icon.icon = self.red_image

    def run(self):
        while self.prosseguir:
            try:
                self.icon.run()
            except Exception as ex:
                pass

    def build_menu(self):
         self.icon.menu = pystray.Menu(
             #self.menu_state,
             self.menu_exit
             )
         
    def stop(self):
        logger.info("pausando a aplicação")
        try:
            keyboard.clear_all_hotkeys()
        except:
            pass
        
        self.on_exit()
        self.menu_state = pystray.MenuItem("Start", self.start) 
        #self.icon.icon = self.green_image
        self.build_menu()


    def on_exit(self):
        logger.info("saindo da aplicação")

       
        self.prosseguir=False
        try:
            self.icon.stop()
        except:
            pass




        

    def hide_terminal(self):
            logger.info('escondendo UI')
            self.UI.hide()
            self.menu_visible = pystray.MenuItem("Mostrar UI",self.show_terminal)
            #win32gui.ShowWindow(self.the_program_to_hide , win32con.SW_HIDE)
            self.build_menu()      

    def show_terminal(self):
            logger.info('mostrando UI')
            self.UI.show()
            self.menu_visible = pystray.MenuItem("Esconder UI",self.hide_terminal)
            win32gui.ShowWindow(self.the_program_to_hide , win32con.SW_SHOW) 
            self.build_menu()

    @tempo_decorrido
    def python_handler(self):
            try:
                logger.info('mode python')
                logger.info('preparando dados')
                clipboard = Engineer.pre_processamento()
                logger.info('perguntando a inteligência artificial')

                response = self.AI.python_responder(f"{clipboard}")
                logger.info('resposta recebida')
                Engineer.pos_processamento(clipboard,response)
            except Exception as ex:
                logger.info(ex)

    @tempo_decorrido
    def chat_handler(self):
            try:
                logger.info('mode chat')
                logger.info('preparando dados')
                clipboard = Engineer.pre_processamento()
                logger.info('perguntando a inteligência artificial')
                response = self.AI.responder(f"{clipboard}")
                logger.info('entregando resposta')
                Engineer.pos_processamento(clipboard,response)
            except Exception as ex:
                logger.info(ex)
                print(ex)

    def change_key(self,key):
        if self.AI != None:
            del self.AI
        self.AI = IA(key,logger)

if __name__ == '__main__':
    app = Gtray()
    app.run()
