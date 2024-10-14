import openai
from pessoal.Escriba import registrador
import configparser
#from time import sleep
# Create a new config parser object
config = configparser.ConfigParser()

# Read in the configuration file
config.read('assets/config.ini',encoding='utf-8')

# Adicionando o handler ao logger


class IA:
    def __init__(self,key,looger_from):
        global logger
        logger = looger_from
        k = None
        openai.api_key = key
    def python_responder(self,prompt):
        prompt = 'código python que ' + prompt
        messages = [{"role": "system", "content": prompt}]

        response = ""
        retry=int(config['GTRAY']['retry_ia'])
        while response == "" and retry>0:
            if retry != int(config['GTRAY']['retry_ia']):
                pass
                #sleep(0.1)
            retry-=1
            try:
                response = openai.chat.completions.create(
                        model=config['GTRAY']['modelo'],
                        messages=messages)
            except:
                logger.warn('request AI failed')
        codigo = self.python_filtro(response.choices[0].message.content)    
        return codigo


    def responder(self,prompt):
        messages = [{"role": "system", "content": prompt}]
        response = ""
        retry=int(config['GTRAY']['retry_ia'])
        while response == "" and retry>0:
            if retry != int(config['GTRAY']['retry_ia']):
                pass
                #sleep(0.1)
            retry-=1
            try:
                response = openai.chat.completions.create(
                        model=config['GTRAY']['modelo'],
                        messages=messages) 
            except Exception as e:
                print('request AI failed:' + str(e))
        resposta = response.choices[0].message.content
        logger.info(f'Reposta: {resposta}')
        return resposta

    def python_filtro(self,coms):
        ini_code = coms.find('```python')
        tag_code = coms.find('```')
        if tag_code<0:
            codigo=coms
            logger.info('sem aspas na resposta da AI')    
        elif ini_code >= 0:
            codigo = coms[ini_code+10:coms[ini_code+10::].find('```')+10+ini_code]
            logger.info("encontrado: '''python")
        elif tag_code >= 0:
            codigo = coms[tag_code+4:coms[tag_code+4::].find('```')+4+tag_code]
            logger.info("encontrado: '''")
        logger.info(f'Resposta: {codigo}')
        return codigo