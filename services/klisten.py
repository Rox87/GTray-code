import keyboard
from time import sleep
import configparser
import itertools
#from PyQt5.QtWidgets import QApplication
# Create a new config parser object
config = configparser.ConfigParser()

# Read in the configuration file
config.read('assets/config.ini',encoding='utf-8')
#faça uma lista de 'f1' a 'f12'
lista_f = ['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12']

#faça uma lista com as letras de a a z
lista_letras_mai = [chr(i) for i in range(ord('A'), ord('Z')+1)]
lista_letras_min = [chr(i+32) for i in range(ord('A'), ord('Z')+1)]
lista_letras = list(itertools.chain(lista_letras_min,lista_letras_mai))
class KListen():
    def __init__(self,UI=None,combo="GTRAY"):
        self.UI = UI
        self.main(combo)
        keyboard.on_press(self.record_key)

    def main(self,combo):
        self.keys = []
        self.retry = 100
        self.combo = combo
        self.flag_sair = False
        self.activated = True        
    def set_activated(self,activated):
        self.activated = activated
    def set_combo(self,combo):
        self.combo = combo

    def record_key(self,event):
        if self.activated == True:
            if event.event_type == "down":
                if event.name == 'esc':
                    print("Gravacao interromida...")
                    self.flag_sair = 1
                if event.name not in self.keys:
                    self.keys.append(event.name)
                    if event.name in lista_letras or event.name in lista_f:
                        print("Combinacao:", self.keys)
                        ck = ""
                        for key in self.keys:
                            ck =  ck + '+' + f"{key}"
                        ck = ck[1::]
                        with open(f"assets/shortcut_{self.combo}.cfg",'w',encoding='utf-8') as f:
                            f.write(ck.upper())
                        if len(ck)>1: 
                           self.flag_sair = 1
                        else:
                           self.keys =[]

        else:
            pass        
    def run(self):
        while (not self.flag_sair and self.retry>0):
            sleep(0.1)
            self.retry-=1
            #if self.UI!=None:
            #    if self.retry%10==0:
            #        self.UI.header_shortcut.setText(f'timeout:{int(self.retry/10)}'))
            #        self.UI.lbl_shortcut.setText('precione uma combinação do teclado')
            #        QApplication.processEvents()
        if self.retry <=0:
            keyboard.press('esc')
        #print(f'keys:{self.keys}')
        self.__init__()

if __name__ == '__main__':
    kl = KListen()
    kl.run()

