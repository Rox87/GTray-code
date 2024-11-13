import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QTextEdit, QPushButton,QFileDialog
import cgen
import pyperclip
import os      
class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Configura o layout vertical
        layout = QVBoxLayout()

        # Primeira caixa de texto (single-line)
        self.textbox1 = QLineEdit(self)
        self.textbox1.setPlaceholderText('Caminho para solução')
        layout.addWidget(self.textbox1)

        self.btn = QPushButton('Selecionar Pasta', self)
        # self.btn.setIcon(QIcon('assets/envio.png'))
        self.btn.clicked.connect(self.openFolderDialog)
        layout.addWidget(self.btn)

        # Segunda caixa de texto (multi-line)
        self.textbox2 = QTextEdit(self)
        self.textbox2.setPlaceholderText('Prompt')
        layout.addWidget(self.textbox2)


        # Configurações da janela principal
        self.setLayout(layout)
        self.setWindowTitle('GTRAY Prompt')
        self.setGeometry(100, 100, 400, 300)
        self.show()

        self.btn2 = QPushButton('Generate', self)
        # self.btn2.setIcon(QIcon('assets/run.jpeg'))
        self.btn2.clicked.connect(self.on_click)
        layout.addWidget(self.btn2)

        self.textbox4 = QLineEdit(self)
        self.textbox4.setPlaceholderText('Command Line')

        layout.addWidget(self.textbox4)

        self.btn3 = QPushButton('Executar', self)
        # self.btn2.setIcon(QIcon('assets/run.jpeg'))
        self.btn3.clicked.connect(self.run)
        layout.addWidget(self.btn3)

        # Primeira caixa de texto (single-line)
        self.textbox3 = QTextEdit(self)
        self.textbox3.setPlaceholderText('Resposta')
        layout.addWidget(self.textbox3)

        

    def openFolderDialog(self): 
        folder_path = QFileDialog.getExistingDirectory(self, 'Selecione uma pasta') 
        if folder_path: 
            self.textbox1.setText(folder_path)
    
    def on_click(self):

        # Ação ao clicar no botão
        dir=self.textbox1.text().replace('"','')
        prompt='main.py é o arquivo pricipal. Se precisar de argumentos use o sys.argv[1] e converta-o para o tipo apropriado. ' + self.textbox2.toPlainText()
        print(f'Diretório: {dir}')
        print(f'Código: {prompt}')
        solucao = cgen.code_ia(dir,prompt)
        print(solucao)
        pyperclip.copy(solucao)
        self.textbox3.setText(solucao)
        self.textbox4.setText(f"python main.py")
        

    def run(self):
        import subprocess
        dir=self.textbox1.text()
        resultado = subprocess.run(self.textbox4.text().replace('main.py',os.path.join(dir,'main.py')), shell=True, capture_output=True, text=True, encoding='utf-8')

        if resultado.returncode == 0:
            # Comando executado com sucesso 
            print("Saída padrão:", resultado.stdout)
            self.textbox3.setText(resultado.stdout)
        else:
            # Comando executado com erro 
            print("Erro padrão:", resultado.stderr)
            self.textbox3.setText(resultado.stderr)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    ex.raise_()
    ex.activateWindow()
    sys.exit(app.exec_())

