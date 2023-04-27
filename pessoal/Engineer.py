import pyperclip
from pynput.keyboard import Key, Controller
from time import sleep
import configparser
# Create a new config parser object
config = configparser.ConfigParser()

# Read in the configuration file
config.read('assets/config.ini',encoding='utf-8')

# Adicionando o handler ao logger

keyboard = Controller()

class Engineer:
    def __init__(self,logger_from):
         global logger
         logger = logger_from

    def pre_processamento(MODE='shortcut_file'):

        with open(config['GTRAY'][MODE],'r') as f:
            shortcut = f.read()
        dados_clipboard = ""
        retry_clip=int(config['GTRAY']['retry_clip'])
        while dados_clipboard == "" and retry_clip>0:
            retry_clip-=1
            with keyboard.pressed(Key.ctrl):
                keyboard.press('c')
                keyboard.release('c')
            sleep(0.1)
            dados_clipboard = pyperclip.paste()
            sleep(0.1)


        
        sleep(0.1)
        if len(dados_clipboard) <=1:
            logger.info('ignorado')
            with keyboard.pressed(Key.ctrl):
                    keyboard.press('z')
                    keyboard.release('z')
            return ""
        #sleep(0.1)
        #dados_clipboard = pyperclip.paste()
        input = dados_clipboard
        retry_clip=int(config['GTRAY']['retry_clip'])
        while dados_clipboard != "Processando" and retry_clip>0:
            retry_clip-=1
            pyperclip.copy("Processando")
            sleep(0.1)
            dados_clipboard = pyperclip.paste()
            sleep(0.1)

        with keyboard.pressed(Key.ctrl):
            keyboard.press('v')
            keyboard.release('v')
        sleep(0.2)
        with keyboard.pressed(Key.ctrl):
            with keyboard.pressed(Key.shift):
                keyboard.press(Key.left)
                keyboard.release(Key.left)
        sleep(0.1)
        logger.info(f"Prompt: {input}")

        return input
    
    def pos_processamento(clipboard,response):
        
        if clipboard[0] != "#":
            clipboard = '#' + clipboard

        pyperclip.copy(clipboard)
        sleep(0.1)
        with keyboard.pressed(Key.ctrl):
                keyboard.press('v')
                keyboard.release('v')
        sleep(0.1)
        
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        #sleep(0.3)
        if response[0:6] == "python":
            response=response[6::]
        
        pyperclip.copy(response)
        sleep(0.1)
        with keyboard.pressed(Key.ctrl):
            keyboard.press('v')
            keyboard.release('v')
        
        
        logger.info('resposta entregue')

