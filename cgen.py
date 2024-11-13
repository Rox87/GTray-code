
import openai
import sys
import os
import re 
with open('assets/k.cfg','r') as f:
    openai.api_key = f.read()

def code_ia(dir,prompt):
    response = openai.chat.completions.create(
                        model='gpt-4o-mini',
                        messages=[{"role": "system", "content": "seja extremamente breve e retorne apenas o nome entre ** seguido do bloco código python correspondente para cada arquivo da solução a seguir: " + prompt}])
    coms = response.choices[0].message.content

    # Padrão regex
    padrao = r'\*\*(.*?)\*\*\n```(.*?)\n(.*?)```'
        
    matches = re.findall(padrao, coms, re.DOTALL)

    # Imprimir as correspondências encontradas
    for match in matches:
        filename, lang, bloco = match
        print(f"Filename: {filename}")
        print(f"Lang: {lang}")
        print(f"Code Block: {bloco}\n")

        dir2 = "\\".join(filename.split("/")[:-1])
        
        # Criar diretórios recursivamente
        final_code = ""
        os.makedirs(os.path.join(dir,dir2), exist_ok=True) 
        with open(os.path.join(dir,filename), 'w', encoding="utf-8") as file:
            final_code += f"#{lang} - {filename}\n{bloco}" + "\n"
            file.write(bloco)
    
    return final_code

if __name__ == '__main__':
    dir = sys.argv[1]
    with open(os.path.join(dir,'input.txt'),'r',encoding='utf-8') as file:
        prompt = file.read()

    code_ia(dir,prompt)