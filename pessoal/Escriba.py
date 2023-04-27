import logging
import configparser
# Create a new config parser object
config = configparser.ConfigParser()

# Read in the configuration file
config.read('assets/config.ini',encoding='utf-8')
class registrador:
    def __init__(self):
        self.logger = logging.getLogger('gtray')
        self.logger.setLevel(logging.INFO)
        self.file_handler = logging.FileHandler(config['GTRAY']['log'])
        self.file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.file_handler.setFormatter(formatter)
    def addHand(self):    
        self.logger.addHandler(self.file_handler)
    def get_logger(self):
        #logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        #logger = logging.getLogger()

        return self.logger
        # Criando um handler para exibir logs no console
        #console_handler = logging.StreamHandler()
        #console_handler.setLevel(logging.INFO)
        #console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))

        # Adicionando o handler ao logger
        #logger.addHandler(console_handler)

        # Criando um handler para gravar logs em arquivo
        file_handler = logging.FileHandler(config['GTRAY']['log'])
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        return logger