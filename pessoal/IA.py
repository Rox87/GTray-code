import openai
import os
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
        import re

        def detectar_caminho_arquivo(texto):
            padrao = r'@@([^@]+[\\/][^@]+)@'
            matches = re.findall(padrao, texto)
            return matches

        # Exemplo de uso
        # texto = r"Aqui está o caminho do arquivo: %*C:\Users\rodri\Documents\Space\develop\python\repos.github.rox87\systray\teste.py*%"
        caminhos_arquivos = detectar_caminho_arquivo(prompt)

        for caminho in caminhos_arquivos:
            try:
                print(f"Caminho do arquivo detectado: {caminho}")
                with open(caminho,'r',encoding='utf-8') as file:
                    prompt += f'\n#{caminho}\n' + file.read()
            except:
                pass

        response = openai.chat.completions.create(
                            model=config['GTRAY']['modelo'],
                            messages=[{"role": "system", "content": "seja extremamente breve e retorne apenas o nome entre ** seguido do bloco código python para cada arquivo da solução a seguir: " + prompt}])
        coms = response.choices[0].message.content
        final_code = f'"""{prompt}"""\n'
        
        # Padrão regex
        padrao = r'\*\*(.*?)\*\*\n```(.*?)\n(.*?)```'           
        matches = re.findall(padrao, coms, re.DOTALL)

        # Imprimir as correspondências encontradas
        for match in matches:
            filename, lang, bloco = match
            print(f"Filename: {filename}")
            print(f"Lang: {lang}")
            print(f"Code Block: {bloco}\n")
            final_code += f'{lang} - {filename}\n{bloco}'

        return final_code


    def responder(self,prompt,cmd=""):
        messages = [{"role": "system", "content": cmd},
                    {"role":"user", "content": prompt}]
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
        response = openai.chat.completions.create(
                            model=config['GTRAY']['modelo'],
                            messages=[{"role": "system", "content": "seja extremamente breve e retorne apenas o nome entre ** seguido do bloco código python correspondente para cada arquivo da solução a seguir: " + coms}])
        coms = response.choices[0].message.content
        final_code = f"#{coms}\n"
        while True:
            nome_inicio = coms.find("**") + 2
            nome_final = coms[nome_inicio:].find("**")
            filename = coms[nome_inicio:][:nome_final]
            print(filename)
            code_inicio = coms.find("```python") + 9
            code_final = coms[code_inicio:].find("```")
            final_code += f'#{filename}\n' + coms[code_inicio:][:code_final]
            # with open('' + filename, 'w') as file: # Escreve algumas linhas no arquivo file.write(
            #     file.write(coms[code_inicio:][:code_final])
            coms = coms[(code_final+3):]
            if coms.find("**") == -1:
                 break

        return final_code