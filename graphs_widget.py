import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QTextEdit, QPushButton,QFileDialog
from PyQt5.QtGui import QIcon
import cgen
import os
import subprocess
        
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
        self.textbox2.setPlaceholderText('Dados')
        layout.addWidget(self.textbox2)


        # Configurações da janela principal
        self.setLayout(layout)
        self.setWindowTitle('GTRAY Graficos')
        self.setGeometry(100, 100, 400, 300)
        self.show()

        self.btn2 = QPushButton('Grafico', self)
        # self.btn2.setIcon(QIcon('assets/run.jpeg'))
        self.btn2.clicked.connect(self.run)
        layout.addWidget(self.btn2)

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
        dir=self.textbox1.text()
        prompt=self.textbox2.toPlainText()
        print(f'Diretório: {dir}')
        print(f'Código: {prompt}')
        solucao = cgen.code_ia(dir,prompt)
        print(solucao)

    def run(self):

        # Ação ao clicar no botão
        dir=self.textbox1.text().replace('"','')
        prompt='main.py é o arquivo principal. Retorne o código python que gere o grafico com os dados a seguir: ' + self.textbox2.toPlainText()
        print(f'Diretório: {dir}')
        print(f'Código: {prompt}')
        solucao = cgen.code_ia(dir,prompt)
        print(f'run: {solucao}')
        self.textbox3.setText(solucao)
        subprocess.run(f"python {os.path.join(dir,'main.py')}", shell=True, capture_output=False, text=True)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    ex.raise_()
    ex.activateWindow()
    sys.exit(app.exec_())

