import pyperclip
from pynput.keyboard import Key, Controller
from time import sleep
from pessoal.config_manager import ConfigManager

keyboard = Controller()

class Engineer:
    def __init__(self, logger_from):
        global logger
        logger = logger_from
        self.config = ConfigManager()
        
    def pre_processamento(self, mode='shortcut_melhore_file'):
        with open(self.config.get('GTRAY', mode), 'r') as f:
            shortcut = f.read()

        dados_clipboard = ""
        retry_clip = self.config.get_clip_retry()

        while dados_clipboard == "" and retry_clip > 0:
            retry_clip -= 1
            with keyboard.pressed(Key.ctrl):
                keyboard.press('c')
                keyboard.release('c')
            sleep(0.1)
            dados_clipboard = pyperclip.paste()
            sleep(0.1)

        if len(dados_clipboard) <= 1:
            logger.info('ignorado')
            with keyboard.pressed(Key.ctrl):
                keyboard.press('z')
                keyboard.release('z')
            return ""

        input = dados_clipboard
        retry_clip = self.config.get_clip_retry()

        while dados_clipboard != "Processando" and retry_clip > 0:
            retry_clip -= 1
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
    
    @staticmethod
    def pos_processamento(clipboard, response):
        pyperclip.copy(response)
        sleep(0.1)
        with keyboard.pressed(Key.ctrl):
            keyboard.press('v')
            keyboard.release('v')
        
        logger.info('resposta entregue')

